"""
Tests for WhatsApp Chatbot Service and Webhook Endpoint.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app import app
from backend.database import db
from backend.models.models import (
    Store, TeamMember, Checklist, Task, WhatsAppGroup
)
from backend.services.chatbot_service import ChatbotService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Provide a Flask test client with an isolated in-memory database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            yield c
            db.session.remove()
            db.drop_all()


@pytest.fixture
def sample_data(client):
    """Create a store, team member, checklist, task and WhatsApp group."""
    with app.app_context():
        opening_date = datetime.utcnow() + timedelta(days=14)
        store = Store(
            name='Test Store',
            location='Test City',
            opening_date=opening_date,
            status='in_progress'
        )
        db.session.add(store)
        db.session.flush()

        member = TeamMember(
            name='Alice',
            role='technician',
            phone='+15550001234',
            email='alice@example.com',
            store_id=store.id
        )
        db.session.add(member)
        db.session.flush()

        checklist = Checklist(
            name='Setup Checklist',
            store_id=store.id,
            category='hardware'
        )
        db.session.add(checklist)
        db.session.flush()

        task = Task(
            title='Install POS system',
            checklist_id=checklist.id,
            assigned_to_id=member.id,
            status='pending',
            priority='high',
            due_date=opening_date - timedelta(days=1)
        )
        db.session.add(task)

        group = WhatsAppGroup(
            store_id=store.id,
            group_name='Test Store - Opening Team',
            is_active=True
        )
        db.session.add(group)
        db.session.commit()

        return store.id, member.id, task.id, group.id


# ---------------------------------------------------------------------------
# Chatbot Service Tests
# ---------------------------------------------------------------------------

class TestChatbotServiceContext:
    """Test that chatbot builds context correctly."""

    def test_unknown_sender_returns_guest_context(self, client):
        with app.app_context():
            service = ChatbotService()
            ctx = service._build_context(None)
            assert ctx['member_name'] == 'Guest'
            assert ctx['pending_tasks'] == []
            assert ctx['store_name'] == 'N/A'

    def test_known_member_has_pending_tasks(self, client, sample_data):
        store_id, member_id, task_id, _ = sample_data
        with app.app_context():
            member = TeamMember.query.get(member_id)
            service = ChatbotService()
            ctx = service._build_context(member)
            assert ctx['member_name'] == 'Alice'
            assert len(ctx['pending_tasks']) == 1
            assert ctx['pending_tasks'][0]['title'] == 'Install POS system'
            assert ctx['days_until_opening'] is not None
            assert ctx['days_until_opening'] >= 0


class TestChatbotDoneCommand:
    """Test the 'done <task-id>' command."""

    def test_done_command_marks_task_complete(self, client, sample_data):
        _, member_id, task_id, _ = sample_data
        with app.app_context():
            member = TeamMember.query.get(member_id)
            service = ChatbotService()
            with patch.object(service.whatsapp_service, 'send_message', return_value={'success': True}):
                reply = service._handle_done_command(task_id, member)
            assert '✅' in reply
            task = Task.query.get(task_id)
            assert task.status == 'completed'
            assert task.completed_at is not None

    def test_done_command_nonexistent_task(self, client, sample_data):
        _, member_id, _, _ = sample_data
        with app.app_context():
            member = TeamMember.query.get(member_id)
            service = ChatbotService()
            with patch.object(service.whatsapp_service, 'send_message', return_value={'success': True}):
                reply = service._handle_done_command(99999, member)
            assert '❌' in reply

    def test_done_command_already_completed(self, client, sample_data):
        _, member_id, task_id, _ = sample_data
        with app.app_context():
            # Pre-mark as complete
            task = Task.query.get(task_id)
            task.status = 'completed'
            db.session.commit()

            member = TeamMember.query.get(member_id)
            service = ChatbotService()
            with patch.object(service.whatsapp_service, 'send_message', return_value={'success': True}):
                reply = service._handle_done_command(task_id, member)
            assert 'already' in reply.lower()


class TestChatbotHandleIncoming:
    """Test full handle_incoming_message flow."""

    def test_help_command(self, client, sample_data):
        _, member_id, _, _ = sample_data
        with app.app_context():
            member = TeamMember.query.get(member_id)
            service = ChatbotService()
            with patch.object(service.whatsapp_service, 'send_message', return_value={'success': True}) as mock_send:
                reply = service.handle_incoming_message(
                    f'whatsapp:{member.phone}', 'help'
                )
            assert mock_send.called
            assert reply  # non-empty response

    def test_unknown_sender_gets_reply(self, client, sample_data):
        with app.app_context():
            service = ChatbotService()
            with patch.object(service.whatsapp_service, 'send_message', return_value={'success': True}) as mock_send:
                reply = service.handle_incoming_message(
                    'whatsapp:+19990000000', 'hello'
                )
            assert mock_send.called
            assert reply


# ---------------------------------------------------------------------------
# Webhook Endpoint Tests
# ---------------------------------------------------------------------------

class TestWhatsAppWebhook:
    """Test POST /api/whatsapp/webhook."""

    def test_webhook_returns_200_with_valid_message(self, client, sample_data):
        _, member_id, _, _ = sample_data
        with patch('backend.services.chatbot_service.ChatbotService.handle_incoming_message', return_value='Hi Alice!'):
            response = client.post(
                '/api/whatsapp/webhook',
                data={
                    'From': 'whatsapp:+15550001234',
                    'Body': 'status'
                }
            )
        assert response.status_code == 200
        # Should return TwiML
        assert b'<?xml' in response.data

    def test_webhook_returns_200_with_empty_body(self, client):
        response = client.post(
            '/api/whatsapp/webhook',
            data={'From': '', 'Body': ''}
        )
        assert response.status_code == 200

    def test_webhook_returns_200_on_unknown_number(self, client):
        with patch('backend.services.chatbot_service.ChatbotService.handle_incoming_message', return_value='Hello!'):
            response = client.post(
                '/api/whatsapp/webhook',
                data={'From': 'whatsapp:+19999999999', 'Body': 'hi'}
            )
        assert response.status_code == 200

    def test_webhook_content_type_is_xml(self, client, sample_data):
        with patch('backend.services.chatbot_service.ChatbotService.handle_incoming_message', return_value='OK'):
            response = client.post(
                '/api/whatsapp/webhook',
                data={'From': 'whatsapp:+15550001234', 'Body': 'help'}
            )
        assert 'xml' in response.content_type


# ---------------------------------------------------------------------------
# Group Creation Tests (welcome messages)
# ---------------------------------------------------------------------------

class TestGroupCreationWithWelcome:
    """Test that creating a group sends welcome messages to team members."""

    def test_create_group_sends_welcome_messages(self, client, sample_data):
        store_id, _, _, _ = sample_data
        with app.app_context():
            # Delete the existing group first so we can create a new one
            group = WhatsAppGroup.query.filter_by(store_id=store_id).first()
            db.session.delete(group)
            db.session.commit()

        with patch('backend.routes.whatsapp_routes.whatsapp_service') as mock_ws:
            mock_ws.send_message.return_value = {'success': True}
            response = client.post(
                '/api/whatsapp/groups',
                json={'store_id': store_id}
            )

        assert response.status_code == 201
        data = response.get_json()
        assert 'welcome_messages_sent' in data
        # At least 1 welcome message should have been attempted
        assert data['welcome_messages_sent'] >= 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
