from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.models import Store, WhatsAppGroup, TeamMember
from backend.services.workflow_service import get_workflow_service
from backend.services.whatsapp_service import WhatsAppService
from backend.services.email_service import get_email_service
from backend.utils.common_utils import parse_iso_datetime
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('stores', __name__, url_prefix='/api/stores')

@bp.route('', methods=['GET'])
def get_stores():
    """Get all stores"""
    stores = Store.query.all()
    return jsonify([store.to_dict() for store in stores]), 200

@bp.route('/<int:store_id>', methods=['GET'])
def get_store(store_id):
    """Get a specific store"""
    store = Store.query.get_or_404(store_id)
    result = store.to_dict()
    
    # Include team members count
    result['team_members_count'] = len(store.team_members)
    
    # Include checklist completion stats
    total_tasks = sum(len(checklist.tasks) for checklist in store.checklists)
    completed_tasks = sum(
        len([task for task in checklist.tasks if task.status == 'completed'])
        for checklist in store.checklists
    )
    result['total_tasks'] = total_tasks
    result['completed_tasks'] = completed_tasks
    result['completion_percentage'] = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return jsonify(result), 200

@bp.route('', methods=['POST'])
def create_store():
    """Create a new store with workflow initialization"""
    data = request.get_json()
    
    try:
        store = Store(
            name=data['name'],
            location=data['location'],
            opening_date=parse_iso_datetime(data['opening_date']),
            status=data.get('status', 'planning'),
            workflow_stage=0
        )
        db.session.add(store)
        db.session.flush()  # Get store ID
        
        # Create inline team members if provided
        inline_members = data.get('team_members', [])
        created_members = []
        for member_data in inline_members:
            if not member_data.get('name') or not member_data.get('phone'):
                logger.warning("Skipping team member with missing name or phone: %s", member_data)
                continue
            member = TeamMember(
                name=member_data['name'],
                role=member_data.get('role', 'team_member'),
                phone=member_data['phone'],
                email=member_data.get('email'),
                store_id=store.id,
                is_active=True
            )
            db.session.add(member)
            created_members.append(member)
        
        if created_members:
            db.session.flush()  # Ensure members have IDs
        
        # Determine responsible user for workflow stage assignment
        responsible_user_id = data.get('responsible_user_id')
        if responsible_user_id is None and created_members:
            responsible_user_id = created_members[0].id
        
        # Initialize workflow stages
        workflow_service = get_workflow_service()
        workflow_service.initialize_workflow(store, responsible_user_id=responsible_user_id)
        
        # Create WhatsApp communication channel record
        whatsapp_service = WhatsAppService()
        group_name = f"Store Opening - {store.name}"
        whatsapp_group = WhatsAppGroup(
            store_id=store.id,
            group_name=group_name,
            is_active=True
        )
        db.session.add(whatsapp_group)
        
        db.session.commit()
        
        # Send welcome message to team members
        welcome_message = f"""🎉 Welcome to {group_name}!

Store: {store.name}
Location: {store.location}
Opening Date: {store.opening_date.strftime('%Y-%m-%d')}

This channel will be used for all communications regarding this store opening project.

The 7-stage workflow process has been initiated:
1. Update nearby store details
2. Complete checklist & send to warehouse
3. Confirm material reached nearby store
4. Confirm material sent to actual store
5. Start installation & update TeamViewer ID
6. Complete final checklist on opening day
7. Store opening complete

Note: To receive WhatsApp messages via Twilio sandbox, each recipient must first join the sandbox by sending the keyword to the Twilio number.

Let's work together to ensure a successful store opening! 🚀
"""
        
        # Send to all team members if they exist
        if store.team_members:
            whatsapp_service.send_message_to_group(
                whatsapp_group,
                welcome_message,
                store.team_members
            )
        
        # Send email notifications
        email_service = get_email_service()
        if store.team_members:
            team_emails = [m.email for m in store.team_members if m.email]
            if team_emails:
                email_service.send_store_creation_email(
                    store.to_dict(),
                    [m.to_dict() for m in store.team_members]
                )
        
        result = store.to_dict()
        result['team_members'] = [m.to_dict() for m in store.team_members]
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:store_id>', methods=['PUT'])
def update_store(store_id):
    """Update a store"""
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            store.name = data['name']
        if 'location' in data:
            store.location = data['location']
        if 'opening_date' in data:
            store.opening_date = parse_iso_datetime(data['opening_date'])
        if 'status' in data:
            store.status = data['status']
        
        store.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(store.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:store_id>', methods=['DELETE'])
def delete_store(store_id):
    """Delete a store"""
    store = Store.query.get_or_404(store_id)
    
    try:
        db.session.delete(store)
        db.session.commit()
        return jsonify({'message': 'Store deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:store_id>/summary', methods=['GET'])
def get_store_summary(store_id):
    """Get comprehensive store summary"""
    store = Store.query.get_or_404(store_id)
    
    # Calculate statistics
    total_tasks = sum(len(checklist.tasks) for checklist in store.checklists)
    completed_tasks = sum(
        len([task for task in checklist.tasks if task.status == 'completed'])
        for checklist in store.checklists
    )
    overdue_tasks = sum(
        len([task for task in checklist.tasks 
             if task.due_date and task.due_date < datetime.utcnow() and task.status != 'completed'])
        for checklist in store.checklists
    )
    
    summary = {
        'store': store.to_dict(),
        'statistics': {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': total_tasks - completed_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_percentage': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'team_members_count': len(store.team_members),
            'checklists_count': len(store.checklists)
        },
        'team_members': [member.to_dict() for member in store.team_members],
        'checklists': [checklist.to_dict() for checklist in store.checklists]
    }
    
    return jsonify(summary), 200
