"""
ML Learning API Routes
Endpoints for self-learning AI capabilities
"""

from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.models import Store, Task, Checklist
from backend.services.ml_learning_service import get_ml_service
from datetime import datetime

bp = Blueprint('ml_learning', __name__, url_prefix='/api/ml')

@bp.route('/learn/store/<int:store_id>', methods=['POST'])
def learn_from_store(store_id):
    """Trigger learning from a completed store"""
    try:
        store = Store.query.get_or_404(store_id)
        
        if store.status != 'completed':
            return jsonify({
                'error': 'Can only learn from completed stores',
                'current_status': store.status
            }), 400
        
        # Gather all tasks
        tasks_data = []
        for checklist in store.checklists:
            for task in checklist.tasks:
                tasks_data.append({
                    'id': task.id,
                    'title': task.title,
                    'status': task.status,
                    'priority': task.priority,
                    'created_at': task.created_at,
                    'completed_at': task.completed_at,
                    'due_date': task.due_date,
                    'assigned_to': task.assigned_to_id,
                    'is_overdue': task.due_date < task.completed_at if task.completed_at and task.due_date else False
                })
        
        store_data = {
            'id': store.id,
            'name': store.name,
            'status': store.status,
            'opening_date': store.opening_date,
            'opened_on_time': True  # Calculate based on actual vs planned
        }
        
        # Trigger learning
        ml_service = get_ml_service()
        result = ml_service.learn_from_completed_store(store_data, tasks_data)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/predict/success/<int:store_id>', methods=['GET'])
def predict_success(store_id):
    """Predict success probability for a store"""
    try:
        store = Store.query.get_or_404(store_id)
        
        # Calculate current features
        total_tasks = 0
        completed_tasks = 0
        overdue_tasks = 0
        high_priority_tasks = 0
        
        team_members = set()
        
        for checklist in store.checklists:
            for task in checklist.tasks:
                total_tasks += 1
                if task.status == 'completed':
                    completed_tasks += 1
                if task.due_date and task.due_date < datetime.utcnow() and task.status != 'completed':
                    overdue_tasks += 1
                if task.priority in ['high', 'critical']:
                    high_priority_tasks += 1
                if task.assigned_to_id:
                    team_members.add(task.assigned_to_id)
        
        features = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completed_tasks / total_tasks if total_tasks > 0 else 0,
            'overdue_tasks': overdue_tasks,
            'high_priority_tasks': high_priority_tasks,
            'team_size': len(team_members)
        }
        
        ml_service = get_ml_service()
        prediction = ml_service.predict_completion_success(features)
        
        return jsonify({
            'store_id': store_id,
            'store_name': store.name,
            'current_features': features,
            'prediction': prediction
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/assess/risk/<int:store_id>', methods=['GET'])
def assess_risk(store_id):
    """Assess risk level for a store using ML"""
    try:
        store = Store.query.get_or_404(store_id)
        
        # Calculate current features
        total_tasks = 0
        completed_tasks = 0
        overdue_tasks = 0
        team_members = set()
        
        for checklist in store.checklists:
            for task in checklist.tasks:
                total_tasks += 1
                if task.status == 'completed':
                    completed_tasks += 1
                if task.due_date and task.due_date < datetime.utcnow() and task.status != 'completed':
                    overdue_tasks += 1
                if task.assigned_to_id:
                    team_members.add(task.assigned_to_id)
        
        features = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completed_tasks / total_tasks if total_tasks > 0 else 0,
            'overdue_tasks': overdue_tasks,
            'team_size': len(team_members)
        }
        
        ml_service = get_ml_service()
        risk_assessment = ml_service.assess_current_risk(features)
        
        return jsonify({
            'store_id': store_id,
            'store_name': store.name,
            'current_features': features,
            'risk_assessment': risk_assessment
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/predict/task-duration', methods=['POST'])
def predict_task_duration():
    """Predict expected duration for a task"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Task title required'}), 400
        
        title = data['title']
        priority = data.get('priority', 'medium')
        
        ml_service = get_ml_service()
        prediction = ml_service.predict_task_duration(title, priority)
        
        return jsonify({
            'task_title': title,
            'task_priority': priority,
            'duration_prediction': prediction
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/insights/success-factors', methods=['GET'])
def get_success_factors():
    """Get insights about success factors"""
    try:
        ml_service = get_ml_service()
        insights = ml_service.get_success_insights()
        
        return jsonify(insights), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/models/stats', methods=['GET'])
def get_model_stats():
    """Get statistics about trained ML models"""
    try:
        ml_service = get_ml_service()
        stats = ml_service.get_model_stats()
        
        return jsonify({
            'models': stats,
            'learning_enabled': ml_service.learning_enabled
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/batch-learn', methods=['POST'])
def batch_learn():
    """Learn from all completed stores"""
    try:
        completed_stores = Store.query.filter_by(status='completed').all()
        
        ml_service = get_ml_service()
        results = []
        
        for store in completed_stores:
            tasks_data = []
            for checklist in store.checklists:
                for task in checklist.tasks:
                    tasks_data.append({
                        'id': task.id,
                        'title': task.title,
                        'status': task.status,
                        'priority': task.priority,
                        'created_at': task.created_at,
                        'completed_at': task.completed_at,
                        'due_date': task.due_date,
                        'assigned_to': task.assigned_to_id,
                        'is_overdue': task.due_date < task.completed_at if task.completed_at and task.due_date else False
                    })
            
            store_data = {
                'id': store.id,
                'name': store.name,
                'status': store.status,
                'opening_date': store.opening_date,
                'opened_on_time': True
            }
            
            result = ml_service.learn_from_completed_store(store_data, tasks_data)
            results.append(result)
        
        return jsonify({
            'stores_processed': len(results),
            'results': results
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
