from flask import Blueprint, request, jsonify
from app import db
from backend.models.models import Checklist, Task, Store, TeamMember
from datetime import datetime

bp = Blueprint('checklists', __name__, url_prefix='/api/checklists')

@bp.route('', methods=['GET'])
def get_checklists():
    """Get all checklists"""
    store_id = request.args.get('store_id', type=int)
    
    if store_id:
        checklists = Checklist.query.filter_by(store_id=store_id).all()
    else:
        checklists = Checklist.query.all()
    
    return jsonify([checklist.to_dict() for checklist in checklists]), 200

@bp.route('/<int:checklist_id>', methods=['GET'])
def get_checklist(checklist_id):
    """Get a specific checklist"""
    checklist = Checklist.query.get_or_404(checklist_id)
    return jsonify(checklist.to_dict()), 200

@bp.route('', methods=['POST'])
def create_checklist():
    """Create a new checklist"""
    data = request.get_json()
    
    try:
        # Verify store exists
        store = Store.query.get_or_404(data['store_id'])
        
        checklist = Checklist(
            name=data['name'],
            description=data.get('description'),
            store_id=data['store_id'],
            category=data.get('category')
        )
        db.session.add(checklist)
        db.session.commit()
        
        return jsonify(checklist.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:checklist_id>', methods=['PUT'])
def update_checklist(checklist_id):
    """Update a checklist"""
    checklist = Checklist.query.get_or_404(checklist_id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            checklist.name = data['name']
        if 'description' in data:
            checklist.description = data['description']
        if 'category' in data:
            checklist.category = data['category']
        
        db.session.commit()
        return jsonify(checklist.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:checklist_id>', methods=['DELETE'])
def delete_checklist(checklist_id):
    """Delete a checklist"""
    checklist = Checklist.query.get_or_404(checklist_id)
    
    try:
        db.session.delete(checklist)
        db.session.commit()
        return jsonify({'message': 'Checklist deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# Task endpoints
@bp.route('/<int:checklist_id>/tasks', methods=['GET'])
def get_tasks(checklist_id):
    """Get all tasks for a checklist"""
    checklist = Checklist.query.get_or_404(checklist_id)
    return jsonify([task.to_dict() for task in checklist.tasks]), 200

@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@bp.route('/<int:checklist_id>/tasks', methods=['POST'])
def create_task(checklist_id):
    """Create a new task"""
    checklist = Checklist.query.get_or_404(checklist_id)
    data = request.get_json()
    
    try:
        task = Task(
            title=data['title'],
            description=data.get('description'),
            checklist_id=checklist_id,
            assigned_to_id=data.get('assigned_to_id'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            due_date=datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')) if data.get('due_date') else None
        )
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    try:
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'assigned_to_id' in data:
            task.assigned_to_id = data['assigned_to_id']
        if 'status' in data:
            task.status = data['status']
            if data['status'] == 'completed' and not task.completed_at:
                task.completed_at = datetime.utcnow()
        if 'priority' in data:
            task.priority = data['priority']
        if 'due_date' in data:
            task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')) if data['due_date'] else None
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(task.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
