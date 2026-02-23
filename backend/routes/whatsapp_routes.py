from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.models import WhatsAppGroup, ArchivedConversation, Store
from backend.services.whatsapp_service import WhatsAppService
from backend.services.chatbot_service import get_chatbot_service
from datetime import datetime

bp = Blueprint('whatsapp', __name__, url_prefix='/api/whatsapp')
whatsapp_service = WhatsAppService()

@bp.route('/groups', methods=['GET'])
def get_groups():
    """Get all WhatsApp groups"""
    groups = WhatsAppGroup.query.all()
    return jsonify([group.to_dict() for group in groups]), 200

@bp.route('/groups/<int:store_id>', methods=['GET'])
def get_group_by_store(store_id):
    """Get WhatsApp group for a specific store"""
    group = WhatsAppGroup.query.filter_by(store_id=store_id).first()
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    return jsonify(group.to_dict()), 200

@bp.route('/groups', methods=['POST'])
def create_group():
    """Create a WhatsApp group for a store and onboard team members"""
    data = request.get_json()
    
    try:
        # Verify store exists
        store = Store.query.get_or_404(data['store_id'])
        
        # Check if group already exists
        existing_group = WhatsAppGroup.query.filter_by(store_id=data['store_id']).first()
        if existing_group:
            return jsonify({'error': 'Group already exists for this store'}), 400
        
        group_name = data.get('group_name', f"{store.name} - Opening Team")
        
        # Create group record
        group = WhatsAppGroup(
            store_id=data['store_id'],
            group_name=group_name,
            is_active=True
        )
        db.session.add(group)
        db.session.commit()
        
        # Note: Twilio does not support programmatic WhatsApp group creation.
        # This record is used to track the communication channel for the store
        # and to broadcast messages individually to team members.

        # Send welcome/onboarding message to all active team members
        welcome_message = (
            f"👋 Welcome to *{group_name}*!\n\n"
            f"You've been added to the WhatsApp communication channel for "
            f"*{store.name}* (opening: {store.opening_date.strftime('%Y-%m-%d')}).\n\n"
            "🤖 *AI Chatbot Commands:*\n"
            "• Send *status* – see your pending tasks\n"
            "• Send *store* – store opening info\n"
            "• Send *done <task-id>* – mark a task complete\n"
            "• Send *help* – show this menu\n\n"
            "You'll receive automated follow-up reminders here. "
            "Reply to this number anytime to interact with the AI assistant!"
        )
        sent = 0
        failed = 0
        for member in store.team_members:
            if member.is_active and member.phone:
                result = whatsapp_service.send_message(member.phone, welcome_message)
                if result.get('success'):
                    sent += 1
                else:
                    failed += 1

        result = group.to_dict()
        result['note'] = (
            'Communication channel record created. '
            'Messages are sent individually to team members via Twilio WhatsApp. '
            'Ensure each recipient has joined the Twilio sandbox first.'
        )
        result['welcome_messages_sent'] = sent
        result['welcome_messages_failed'] = failed
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/groups/<int:group_id>/send', methods=['POST'])
def send_message(group_id):
    """Send a message to a WhatsApp group"""
    group = WhatsAppGroup.query.get_or_404(group_id)
    data = request.get_json()
    
    try:
        message = data.get('message')
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get team members for this store
        team_members = group.store.team_members
        
        # Send message via WhatsApp service
        result = whatsapp_service.send_message_to_group(group, message, team_members)
        
        return jsonify({
            'message': 'Message sent successfully',
            'sent_to': result.get('sent_to', 0),
            'failed': result.get('failed', 0)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/groups/<int:group_id>/archive', methods=['POST'])
def archive_group(group_id):
    """Archive group conversations before deletion"""
    group = WhatsAppGroup.query.get_or_404(group_id)
    data = request.get_json()
    
    try:
        # Archive conversations (in production, this would fetch from Twilio)
        conversations = data.get('conversations', [])
        
        for conv in conversations:
            archived = ArchivedConversation(
                group_id=group.id,
                sender=conv.get('sender', 'Unknown'),
                message=conv.get('message', ''),
                timestamp=datetime.fromisoformat(conv['timestamp'].replace('Z', '+00:00')) if conv.get('timestamp') else datetime.utcnow(),
                message_type=conv.get('message_type', 'text')
            )
            db.session.add(archived)
        
        group.is_active = False
        group.archived_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Group archived successfully',
            'archived_messages': len(conversations)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/groups/<int:group_id>/archive', methods=['GET'])
def get_archived_conversations(group_id):
    """Get archived conversations for a group"""
    group = WhatsAppGroup.query.get_or_404(group_id)
    conversations = ArchivedConversation.query.filter_by(group_id=group_id).order_by(ArchivedConversation.timestamp).all()
    
    return jsonify({
        'group': group.to_dict(),
        'conversations': [conv.to_dict() for conv in conversations]
    }), 200

@bp.route('/send-follow-up', methods=['POST'])
def send_follow_up():
    """Send a follow-up message for a task"""
    data = request.get_json()
    
    try:
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({'error': 'Phone and message are required'}), 400
        
        result = whatsapp_service.send_message(phone, message)
        
        return jsonify({
            'message': 'Follow-up sent successfully',
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/diagnostics', methods=['GET'])
def diagnostics():
    """
    Return diagnostics about the WhatsApp/Twilio configuration.
    Useful for verifying credentials, TEST_MODE, and phone number setup.
    """
    import os
    service = WhatsAppService()
    number = service.whatsapp_number or ''
    # Show enough of the number to identify it while masking middle digits
    bare = number.replace('whatsapp:', '')
    if len(bare) >= 6:
        masked_number = bare[:4] + '****' + bare[-3:]
    elif bare:
        masked_number = '****'
    else:
        masked_number = ''
    return jsonify({
        'twilio_initialized': service.client is not None,
        'test_mode': service.test_mode,
        'whatsapp_number': masked_number,
        'account_sid_set': bool(service.account_sid),
        'auth_token_set': bool(service.auth_token),
        'notes': (
            'Twilio client is active. Ensure recipients have joined the sandbox '
            '(send "join <sandbox-keyword>" to the WhatsApp number).'
            if service.client else
            'TEST MODE active – messages are logged only, not sent via Twilio.'
            if service.test_mode else
            'Twilio credentials not configured. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.'
        )
    }), 200


@bp.route('/send-template', methods=['POST'])
def send_template():
    """Send a WhatsApp template message using ContentSid"""
    data = request.get_json()
    
    try:
        phone = data.get('phone')
        content_sid = data.get('content_sid')
        content_variables = data.get('content_variables', {})
        
        if not phone:
            return jsonify({'error': 'Phone number is required'}), 400
        
        if not content_sid:
            return jsonify({'error': 'Content SID is required'}), 400
        
        result = whatsapp_service.send_message(
            to_phone=phone,
            content_sid=content_sid,
            content_variables=content_variables
        )
        
        return jsonify({
            'message': 'Template message sent successfully',
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """
    Twilio webhook for incoming WhatsApp messages.

    Twilio calls this URL (configured in the Twilio Console as the
    'A Message Comes In' webhook for your WhatsApp number) whenever a
    team member sends a WhatsApp message to the Twilio number.

    The chatbot service processes the message, queries the database for
    relevant task/store context, generates an AI reply, and sends it
    back to the sender via the Twilio REST API.

    Returns an empty TwiML response (200 OK) so Twilio knows the webhook
    was handled successfully.
    """
    # Twilio sends form-encoded data
    from_number = request.form.get('From', '')
    body = request.form.get('Body', '').strip()

    if not from_number or not body:
        # Return empty TwiML – nothing to process
        return _twiml_response(''), 200

    try:
        chatbot = get_chatbot_service()
        chatbot.handle_incoming_message(from_number, body)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Webhook processing error: {e}")

    # Always return an empty TwiML 200 so Twilio doesn't retry
    return _twiml_response(''), 200


def _twiml_response(message: str) -> str:
    """Return a minimal TwiML response body."""
    from flask import make_response
    if message:
        twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{message}</Message></Response>'
    else:
        twiml = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
    resp = make_response(twiml, 200)
    resp.headers['Content-Type'] = 'text/xml'
    return resp
