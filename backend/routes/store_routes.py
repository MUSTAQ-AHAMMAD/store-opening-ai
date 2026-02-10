from flask import Blueprint, request, jsonify
from app import db
from backend.models.models import Store
from datetime import datetime

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
    """Create a new store"""
    data = request.get_json()
    
    try:
        store = Store(
            name=data['name'],
            location=data['location'],
            opening_date=datetime.fromisoformat(data['opening_date'].replace('Z', '+00:00')),
            status=data.get('status', 'planning')
        )
        db.session.add(store)
        db.session.commit()
        
        return jsonify(store.to_dict()), 201
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
            store.opening_date = datetime.fromisoformat(data['opening_date'].replace('Z', '+00:00'))
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
