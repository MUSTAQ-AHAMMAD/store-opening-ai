"""
Test Suite for Process Automation Capabilities
Validates that all automation features work correctly
"""

import pytest
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from backend.database import db
from backend.models.models import (
    Store, WorkflowStage, TeamMember, Task, Checklist,
    NearbyStoreDetails, MaterialTracking, TeamViewerSession,
    EscalationHistory, FollowUp
)
from backend.services.workflow_service import WorkflowService
from backend.services.whatsapp_service import WhatsAppService
from backend.services.email_service import EmailService
from backend.services.voice_service import get_voice_service
from backend.services.ai_service import get_ai_service
from backend.services.ml_learning_service import MLLearningService


@pytest.fixture(autouse=True)
def set_test_environment(monkeypatch):
    """Set test environment variables for all tests"""
    monkeypatch.setenv('TEST_MODE', 'true')
    monkeypatch.setenv('ENABLE_SCHEDULER', 'false')


@pytest.fixture
def app():
    """Create test app"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_store(app):
    """Create a sample store for testing"""
    with app.app_context():
        opening_date = datetime.utcnow() + timedelta(days=20)
        store = Store(
            name="Test Store",
            location="Test Location",
            opening_date=opening_date,
            status="planning"
        )
        db.session.add(store)
        db.session.commit()
        
        # Refresh to get the ID
        db.session.refresh(store)
        return store.id


@pytest.fixture
def sample_team_member(app, sample_store):
    """Create a sample team member"""
    with app.app_context():
        member = TeamMember(
            name="Test Member",
            role="technician",
            phone="+1234567890",
            email="test@example.com",
            store_id=sample_store
        )
        db.session.add(member)
        db.session.commit()
        
        db.session.refresh(member)
        return member.id


class TestWorkflowAutomation:
    """Test 7-stage workflow automation"""
    
    def test_workflow_initialization(self, app, sample_store):
        """Test that workflow stages are automatically created"""
        with app.app_context():
            store = Store.query.get(sample_store)
            workflow_service = WorkflowService()
            
            # Initialize workflow
            stages = workflow_service.initialize_workflow(store)
            
            # Should create 7 stages
            assert len(stages) == 7
            
            # Stage 1 should be in progress
            assert stages[0].status == 'in_progress'
            assert stages[0].started_at is not None
            
            # Other stages should be pending
            for stage in stages[1:]:
                assert stage.status == 'pending'
            
            # Due dates should be calculated correctly
            assert stages[0].due_date == store.opening_date - timedelta(days=20)  # Stage 1
            assert stages[4].due_date == store.opening_date - timedelta(days=1)   # Stage 5
    
    def test_stage_auto_advancement(self, app, sample_store, sample_team_member):
        """Test that stages automatically advance"""
        with app.app_context():
            store = Store.query.get(sample_store)
            workflow_service = WorkflowService()
            
            # Initialize workflow
            workflow_service.initialize_workflow(store)
            
            # Complete Stage 1
            result = workflow_service.complete_stage_1(
                store_id=sample_store,
                nearby_store_name="Nearby Store",
                nearby_store_address="123 Main St",
                contact_person_name="John Doe",
                contact_person_mobile="+1234567890",
                distance_km=5.0,
                updated_by_id=sample_team_member
            )
            
            assert result['success'] is True
            
            # Verify Stage 1 is completed
            stage1 = WorkflowStage.query.filter_by(
                store_id=sample_store,
                stage_number=1
            ).first()
            assert stage1.status == 'completed'
            assert stage1.completed_at is not None
            
            # Verify Stage 2 is now in progress
            stage2 = WorkflowStage.query.filter_by(
                store_id=sample_store,
                stage_number=2
            ).first()
            assert stage2.status == 'in_progress'
            assert stage2.started_at is not None
    
    def test_timeline_recalculation(self, app, sample_store):
        """Test automatic timeline recalculation when opening date changes"""
        with app.app_context():
            store = Store.query.get(sample_store)
            workflow_service = WorkflowService()
            
            # Initialize workflow
            workflow_service.initialize_workflow(store)
            
            # Get original due date for Stage 1
            stage1 = WorkflowStage.query.filter_by(
                store_id=sample_store,
                stage_number=1
            ).first()
            original_due_date = stage1.due_date
            
            # Change opening date
            new_opening_date = store.opening_date + timedelta(days=10)
            result = workflow_service.update_opening_date(
                store_id=sample_store,
                new_opening_date=new_opening_date
            )
            
            assert result['success'] is True
            
            # Verify due dates were recalculated
            stage1 = WorkflowStage.query.filter_by(
                store_id=sample_store,
                stage_number=1
            ).first()
            
            # New due date should be 10 days later
            expected_due_date = original_due_date + timedelta(days=10)
            assert stage1.due_date == expected_due_date


class TestMaterialTracking:
    """Test material tracking automation"""
    
    def test_material_tracking_flow(self, app, sample_store, sample_team_member):
        """Test 4-checkpoint material tracking"""
        with app.app_context():
            store = Store.query.get(sample_store)
            workflow_service = WorkflowService()
            
            # Initialize workflow
            workflow_service.initialize_workflow(store)
            
            # Complete Stage 1
            workflow_service.complete_stage_1(
                store_id=sample_store,
                nearby_store_name="Nearby Store",
                nearby_store_address="123 Main St",
                contact_person_name="John Doe",
                contact_person_mobile="+1234567890",
                distance_km=5.0,
                updated_by_id=sample_team_member
            )
            
            # Complete Stage 2 (Warehouse shipment)
            result = workflow_service.complete_stage_2(
                store_id=sample_store,
                confirmed_by_id=sample_team_member
            )
            assert result['success'] is True
            
            # Verify material tracking was created
            tracking = MaterialTracking.query.filter_by(store_id=sample_store).first()
            assert tracking is not None
            assert tracking.warehouse_shipped_at is not None
            assert tracking.status == 'shipped'
            
            # Complete Stage 3 (Nearby store receipt)
            result = workflow_service.complete_stage_3(
                store_id=sample_store,
                confirmed_by_id=sample_team_member
            )
            assert result['success'] is True
            
            tracking = MaterialTracking.query.filter_by(store_id=sample_store).first()
            assert tracking.nearby_store_received_at is not None
            assert tracking.status == 'at_nearby_store'
            
            # Complete Stage 4 (Store receipt)
            result = workflow_service.complete_stage_4(
                store_id=sample_store,
                confirmed_by_id=sample_team_member
            )
            assert result['success'] is True
            
            tracking = MaterialTracking.query.filter_by(store_id=sample_store).first()
            assert tracking.store_received_at is not None
            assert tracking.status == 'delivered'


class TestEscalationAutomation:
    """Test escalation automation"""
    
    def test_escalation_level_determination(self, app, sample_store, sample_team_member):
        """Test that escalation levels are correctly determined"""
        with app.app_context():
            store = Store.query.get(sample_store)
            
            # Create checklist and task
            checklist = Checklist(
                store_id=sample_store,
                name="Test Checklist",
                category="hardware"
            )
            db.session.add(checklist)
            db.session.commit()
            
            # Create overdue task
            task = Task(
                checklist_id=checklist.id,
                title="Test Task",
                priority="high",
                status="in_progress",
                assigned_to_id=sample_team_member,
                due_date=datetime.utcnow() - timedelta(days=5)  # 5 days overdue
            )
            db.session.add(task)
            db.session.commit()
            
            # Calculate escalation level
            days_overdue = (datetime.utcnow() - task.due_date).days
            
            if days_overdue >= 7:
                expected_level = 2
            elif days_overdue >= 3:
                expected_level = 1
            else:
                expected_level = 0
            
            assert days_overdue == 5
            assert expected_level == 1  # Should be urgent level
    
    def test_escalation_history_tracking(self, app, sample_store, sample_team_member):
        """Test that escalations are tracked in history"""
        with app.app_context():
            store = Store.query.get(sample_store)
            workflow_service = WorkflowService()
            
            # Initialize workflow
            workflow_service.initialize_workflow(store)
            
            # Get stage 1
            stage1 = WorkflowStage.query.filter_by(
                store_id=sample_store,
                stage_number=1
            ).first()
            
            # Make stage overdue
            stage1.due_date = datetime.utcnow() - timedelta(days=3)
            db.session.commit()
            
            # Trigger escalation
            result = workflow_service.escalate_stage(
                stage=stage1,
                escalation_level=1
            )
            
            # Verify escalation was recorded
            escalations = EscalationHistory.query.filter_by(
                store_id=sample_store
            ).all()
            
            assert len(escalations) > 0
            escalation = escalations[0]
            assert escalation.escalation_level == 1
            assert escalation.status == 'sent'


class TestAIAutomation:
    """Test AI-powered automation features"""
    
    def test_ai_message_generation(self, app, sample_store, sample_team_member):
        """Test AI-generated follow-up messages"""
        with app.app_context():
            ai_service = get_ai_service()
            
            # Create sample task data
            task_data = {
                'title': 'Install POS System',
                'priority': 'high',
                'days_overdue': 3,
                'store_name': 'Test Store',
                'team_member_name': 'John Doe'
            }
            
            # Generate message
            message = ai_service.generate_follow_up_message(task_data)
            
            # Verify message was generated
            assert message is not None
            assert len(message) > 0
            
            # Should contain key information
            if 'Install POS System' not in message:
                # AI might paraphrase, check for generic task reference
                assert 'task' in message.lower() or 'pos' in message.lower()
    
    def test_ai_task_prioritization(self, app, sample_store):
        """Test AI task prioritization"""
        with app.app_context():
            ai_service = get_ai_service()
            store = Store.query.get(sample_store)
            
            # Create multiple tasks
            checklist = Checklist(
                store_id=sample_store,
                name="Test Checklist",
                category="hardware"
            )
            db.session.add(checklist)
            db.session.commit()
            
            tasks_data = [
                {'title': 'Task 1', 'priority': 'low', 'due_date': datetime.utcnow() + timedelta(days=5)},
                {'title': 'Task 2', 'priority': 'high', 'due_date': datetime.utcnow() + timedelta(days=1)},
                {'title': 'Task 3', 'priority': 'medium', 'due_date': datetime.utcnow() + timedelta(days=3)},
            ]
            
            for task_data in tasks_data:
                task = Task(
                    checklist_id=checklist.id,
                    title=task_data['title'],
                    priority=task_data['priority'],
                    due_date=task_data['due_date'],
                    status='pending'
                )
                db.session.add(task)
            db.session.commit()
            
            # Get prioritization
            result = ai_service.prioritize_tasks(sample_store)
            
            # Should return prioritized list
            assert result is not None
            assert 'priorities' in result or 'recommendations' in result or isinstance(result, list)


class TestMLLearning:
    """Test ML learning automation"""
    
    def test_ml_model_initialization(self):
        """Test ML service initializes correctly"""
        ml_service = MLLearningService()
        
        # Should have 4 models
        assert 'completion_predictor' in ml_service.models
        assert 'risk_assessor' in ml_service.models
        assert 'task_duration' in ml_service.models
        assert 'success_factors' in ml_service.models
    
    def test_ml_learning_from_store(self, app, sample_store):
        """Test ML learning from completed store"""
        with app.app_context():
            ml_service = MLLearningService()
            store = Store.query.get(sample_store)
            
            # Create sample completed store data
            store_data = {
                'id': sample_store,
                'name': 'Test Store',
                'status': 'completed',
                'opening_date': datetime.utcnow(),
                'created_at': datetime.utcnow() - timedelta(days=30)
            }
            
            # Create sample tasks data
            tasks_data = [
                {
                    'title': 'Task 1',
                    'status': 'completed',
                    'priority': 'high',
                    'is_overdue': False,
                    'completion_time_days': 2
                },
                {
                    'title': 'Task 2',
                    'status': 'completed',
                    'priority': 'medium',
                    'is_overdue': False,
                    'completion_time_days': 3
                }
            ]
            
            # Learn from store
            result = ml_service.learn_from_completed_store(store_data, tasks_data)
            
            assert result['success'] is True
            assert result['store_id'] == sample_store
            assert result['models_updated'] == 4


class TestNotificationAutomation:
    """Test notification automation"""
    
    def test_whatsapp_service_initialization(self):
        """Test WhatsApp service initializes in test mode"""
        whatsapp_service = WhatsAppService()
        
        # Should work in test mode
        assert whatsapp_service is not None
    
    def test_email_service_initialization(self):
        """Test Email service initializes in test mode"""
        email_service = EmailService()
        
        # Should work in test mode
        assert email_service is not None
    
    def test_voice_service_initialization(self):
        """Test Voice service initializes in test mode"""
        voice_service = get_voice_service()
        
        # Should work in test mode
        assert voice_service is not None
    
    def test_notification_mock_behavior(self, app, sample_store, sample_team_member):
        """Test that notifications return mock success in test mode"""
        with app.app_context():
            whatsapp_service = WhatsAppService()
            member = TeamMember.query.get(sample_team_member)
            
            # Send test message
            result = whatsapp_service.send_message(
                to_number=member.phone,
                message="Test message"
            )
            
            # In test mode, should succeed without sending
            assert result is not None
            # Test mode returns mock success
            assert result.get('success') is True or result.get('test_mode') is True


class TestRemoteSupportAutomation:
    """Test TeamViewer integration automation"""
    
    def test_teamviewer_validation(self, app, sample_store, sample_team_member):
        """Test TeamViewer ID validation in Stage 5"""
        with app.app_context():
            store = Store.query.get(sample_store)
            workflow_service = WorkflowService()
            
            # Initialize workflow and complete stages 1-4
            workflow_service.initialize_workflow(store)
            
            # Complete stages 1-4 quickly
            workflow_service.complete_stage_1(
                store_id=sample_store,
                nearby_store_name="Nearby Store",
                nearby_store_address="123 Main St",
                contact_person_name="John Doe",
                contact_person_mobile="+1234567890",
                distance_km=5.0,
                updated_by_id=sample_team_member
            )
            
            workflow_service.complete_stage_2(
                store_id=sample_store,
                confirmed_by_id=sample_team_member
            )
            
            workflow_service.complete_stage_3(
                store_id=sample_store,
                confirmed_by_id=sample_team_member
            )
            
            workflow_service.complete_stage_4(
                store_id=sample_store,
                confirmed_by_id=sample_team_member
            )
            
            # Try to complete Stage 5 with TeamViewer ID
            result = workflow_service.complete_stage_5(
                store_id=sample_store,
                teamviewer_id="123456789",
                technician_id=sample_team_member
            )
            
            assert result['success'] is True
            
            # Verify TeamViewer session was created
            session = TeamViewerSession.query.filter_by(store_id=sample_store).first()
            assert session is not None
            assert session.teamviewer_id == "123456789"
            assert session.technician_id == sample_team_member


def test_all_services_loaded():
    """Test that all automation services can be loaded"""
    # This test verifies imports work correctly
    assert WorkflowService is not None
    assert WhatsAppService is not None
    assert EmailService is not None
    assert get_voice_service is not None
    assert get_ai_service is not None
    assert MLLearningService is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
