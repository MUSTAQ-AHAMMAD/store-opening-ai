from flask import Blueprint, request, jsonify
from app import db
from backend.models.models import WhatsAppGroup, ArchivedConversation, Store
from backend.services.whatsapp_service import WhatsAppService
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
    """Create a WhatsApp group for a store"""
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
        
        # Note: Actual WhatsApp group creation would happen via Twilio API
        # For now, we're just tracking it in our database
        
        return jsonify(group.to_dict()), 201
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
