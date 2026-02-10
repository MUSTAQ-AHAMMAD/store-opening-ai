"""
Voice Calling Routes
Handles voice call escalations and acknowledgments
"""

from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.models import Task, TeamMember, Store, FollowUp
from backend.services.voice_service import get_voice_service
from datetime import datetime

bp = Blueprint('voice', __name__, url_prefix='/api/voice')

@bp.route('/escalate/task/<int:task_id>', methods=['POST'])
def escalate_task_by_call(task_id):
    """Make a voice call escalation for a specific task"""
    try:
        task = Task.query.get_or_404(task_id)
        
        if not task.assigned_to:
            return jsonify({'error': 'Task has no assignee'}), 400
        
        # Get store context
        store = Store.query.join(Checklist).filter(Checklist.id == task.checklist_id).first()
        
        if not store:
            return jsonify({'error': 'Store not found'}), 404
        
        # Calculate days overdue
        days_overdue = 0
        if task.due_date:
            days_overdue = (datetime.utcnow() - task.due_date).days
        
        # Determine escalation level
        data = request.get_json() or {}
        escalation_level = data.get('escalation_level', 1)
        
        # Make the call
        voice_service = get_voice_service()
        result = voice_service.make_escalation_call(
            recipient_phone=task.assigned_to.phone,
            recipient_name=task.assigned_to.name,
            task_title=task.title,
            escalation_level=escalation_level,
            store_name=store.name,
            days_overdue=days_overdue
        )
        
        if result['success']:
            # Log the escalation
            follow_up = FollowUp(
                task_id=task.id,
                scheduled_time=datetime.utcnow(),
                message=f"Voice call escalation (Level {escalation_level})",
                status='sent',
                sent_at=datetime.utcnow(),
                escalation_level=escalation_level
            )
            db.session.add(follow_up)
            db.session.commit()
            
            return jsonify({
                'message': 'Escalation call initiated successfully',
                'call_sid': result['call_sid'],
                'status': result['status']
            }), 200
        else:
            return jsonify({
                'error': 'Failed to initiate call',
                'details': result.get('error')
            }), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/escalate/manager/<int:task_id>', methods=['POST'])
def escalate_to_manager(task_id):
    """Escalate a task to the manager via voice call"""
    try:
        from backend.models.models import Checklist
        
        task = Task.query.get_or_404(task_id)
        
        # Get store and find manager
        store = Store.query.join(Checklist).filter(Checklist.id == task.checklist_id).first()
        
        if not store:
            return jsonify({'error': 'Store not found'}), 404
        
        # Find a manager for this store
        manager = TeamMember.query.filter(
            TeamMember.store_id == store.id,
            TeamMember.role.in_(['manager', 'store_manager'])
        ).first()
        
        if not manager:
            return jsonify({'error': 'No manager found for this store'}), 404
        
        # Calculate days overdue
        days_overdue = 0
        if task.due_date:
            days_overdue = (datetime.utcnow() - task.due_date).days
        
        # Make the manager escalation call
        voice_service = get_voice_service()
        result = voice_service.make_manager_escalation_call(
            manager_phone=manager.phone,
            manager_name=manager.name,
            team_member_name=task.assigned_to.name if task.assigned_to else 'Unknown',
            task_title=task.title,
            store_name=store.name,
            days_overdue=days_overdue
        )
        
        if result['success']:
            # Log the manager escalation
            follow_up = FollowUp(
                task_id=task.id,
                scheduled_time=datetime.utcnow(),
                message=f"Manager escalation call to {manager.name}",
                status='sent',
                sent_at=datetime.utcnow(),
                escalation_level=2  # Manager escalations are always level 2
            )
            db.session.add(follow_up)
            db.session.commit()
            
            return jsonify({
                'message': 'Manager escalation call initiated successfully',
                'call_sid': result['call_sid'],
                'manager': manager.name
            }), 200
        else:
            return jsonify({
                'error': 'Failed to initiate manager call',
                'details': result.get('error')
            }), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/acknowledgment', methods=['POST'])
def handle_acknowledgment():
    """Handle voice call acknowledgment from team member"""
    try:
        # Get the digit pressed
        digit = request.values.get('Digits')
        call_sid = request.values.get('CallSid')
        
        from twilio.twiml.voice_response import VoiceResponse
        
        response = VoiceResponse()
        
        if digit == '1':
            # Acknowledged
            response.say(
                "Thank you for acknowledging this escalation. Please log in to the dashboard to update the task status. Goodbye.",
                voice='alice',
                language='en-US'
            )
        elif digit == '2':
            # Request support
            response.say(
                "A support request has been logged. Someone from the team will contact you shortly. Goodbye.",
                voice='alice',
                language='en-US'
            )
        else:
            response.say("Invalid input. Please check your dashboard. Goodbye.", voice='alice', language='en-US')
        
        return str(response), 200, {'Content-Type': 'text/xml'}
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/manager-acknowledgment', methods=['POST'])
def handle_manager_acknowledgment():
    """Handle manager acknowledgment"""
    try:
        from twilio.twiml.voice_response import VoiceResponse
        
        digit = request.values.get('Digits')
        
        response = VoiceResponse()
        
        if digit == '1':
            response.say(
                "Thank you for acknowledging this manager escalation. The system has been updated. Goodbye.",
                voice='alice',
                language='en-US'
            )
        else:
            response.say("Please check your dashboard for details. Goodbye.", voice='alice', language='en-US')
        
        return str(response), 200, {'Content-Type': 'text/xml'}
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/call-status/<call_sid>', methods=['GET'])
def get_call_status(call_sid):
    """Get the status of a voice call"""
    try:
        voice_service = get_voice_service()
        status = voice_service.get_call_status(call_sid)
        
        return jsonify(status), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/test-call', methods=['POST'])
def test_call():
    """Test endpoint for voice calling"""
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data:
            return jsonify({'error': 'Phone number required'}), 400
        
        voice_service = get_voice_service()
        
        result = voice_service.make_escalation_call(
            recipient_phone=data['phone'],
            recipient_name=data.get('name', 'Test User'),
            task_title='Test Task',
            escalation_level=1,
            store_name='Test Store',
            days_overdue=5
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
