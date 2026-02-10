"""
AI-Enhanced Analytics Routes
Provides intelligent insights and predictions
"""

from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.models import Task, Store, TeamMember
from backend.services.ai_service import get_ai_service
from datetime import datetime, timedelta

bp = Blueprint('ai_analytics', __name__, url_prefix='/api/ai')

@bp.route('/task/<int:task_id>/risk-assessment', methods=['GET'])
def get_task_risk_assessment(task_id):
    """Get AI-powered risk assessment for a task"""
    try:
        task = Task.query.get_or_404(task_id)
        
        # Get similar tasks for comparison
        similar_tasks = Task.query.filter(
            Task.priority == task.priority,
            Task.status == 'completed',
            Task.id != task.id
        ).limit(20).all()
        
        # Convert to dict
        similar_tasks_data = []
        for t in similar_tasks:
            completion_days = 0
            completed_on_time = False
            
            if t.completed_at and t.created_at:
                completion_days = (t.completed_at - t.created_at).days
                if t.due_date:
                    completed_on_time = t.completed_at <= t.due_date
            
            similar_tasks_data.append({
                'completion_days': completion_days,
                'completed_on_time': completed_on_time,
                'priority': t.priority
            })
        
        ai_service = get_ai_service()
        risk_assessment = ai_service.predict_task_risk(
            task.to_dict(),
            similar_tasks_data
        )
        
        return jsonify({
            'task_id': task_id,
            'task_title': task.title,
            'risk_assessment': risk_assessment,
            'similar_tasks_analyzed': len(similar_tasks_data)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/store/<int:store_id>/task-prioritization', methods=['GET'])
def get_task_prioritization(store_id):
    """Get AI-suggested task prioritization for a store"""
    try:
        from backend.models.models import Checklist
        
        store = Store.query.get_or_404(store_id)
        
        # Get all pending tasks for the store
        tasks = []
        for checklist in store.checklists:
            for task in checklist.tasks:
                if task.status != 'completed':
                    tasks.append(task.to_dict())
        
        if not tasks:
            return jsonify({
                'message': 'No pending tasks found',
                'tasks': []
            }), 200
        
        # Calculate store context
        days_until_opening = None
        if store.opening_date:
            days_until_opening = (store.opening_date - datetime.utcnow()).days
        
        store_context = {
            'days_until_opening': days_until_opening,
            'store_name': store.name,
            'status': store.status
        }
        
        # Get AI suggestions
        ai_service = get_ai_service()
        prioritized_tasks = ai_service.suggest_task_prioritization(tasks, store_context)
        
        return jsonify({
            'store_id': store_id,
            'store_name': store.name,
            'days_until_opening': days_until_opening,
            'tasks': prioritized_tasks[:10],  # Return top 10
            'ai_enabled': ai_service.enabled
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/task/<int:task_id>/generate-followup', methods=['POST'])
def generate_followup_message(task_id):
    """Generate AI-powered follow-up message"""
    try:
        from backend.models.models import Checklist
        
        task = Task.query.get_or_404(task_id)
        
        if not task.assigned_to:
            return jsonify({'error': 'Task has no assignee'}), 400
        
        # Get store context
        store = Store.query.join(Checklist).filter(Checklist.id == task.checklist_id).first()
        
        if not store:
            return jsonify({'error': 'Store not found'}), 404
        
        # Calculate context
        days_overdue = 0
        if task.due_date:
            days_overdue = max(0, (datetime.utcnow() - task.due_date).days)
        
        days_until_opening = None
        if store.opening_date:
            days_until_opening = (store.opening_date - datetime.utcnow()).days
        
        # Calculate completion percentage
        total_tasks = sum(len(checklist.tasks) for checklist in store.checklists)
        completed_tasks = sum(
            len([t for t in checklist.tasks if t.status == 'completed'])
            for checklist in store.checklists
        )
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        context = {
            'days_overdue': days_overdue,
            'store_opening_date': store.opening_date.strftime('%Y-%m-%d') if store.opening_date else 'TBD',
            'days_until_opening': days_until_opening,
            'completion_percentage': completion_percentage
        }
        
        # Generate message using AI
        ai_service = get_ai_service()
        message = ai_service.generate_follow_up_message(
            task.to_dict(),
            task.assigned_to.to_dict(),
            context
        )
        
        return jsonify({
            'task_id': task_id,
            'message': message,
            'context': context,
            'ai_generated': ai_service.enabled
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/insights/dashboard', methods=['GET'])
def get_ai_insights():
    """Get AI-powered insights for the dashboard"""
    try:
        # Get all active stores
        stores = Store.query.filter(Store.status.in_(['planning', 'in_progress'])).all()
        
        insights = []
        
        for store in stores:
            # Calculate metrics
            total_tasks = sum(len(checklist.tasks) for checklist in store.checklists)
            completed_tasks = sum(
                len([t for t in checklist.tasks if t.status == 'completed'])
                for checklist in store.checklists
            )
            overdue_tasks = sum(
                len([t for t in checklist.tasks 
                     if t.due_date and t.due_date < datetime.utcnow() and t.status != 'completed'])
                for checklist in store.checklists
            )
            
            days_until_opening = None
            if store.opening_date:
                days_until_opening = (store.opening_date - datetime.utcnow()).days
            
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            # Determine risk level
            risk_level = 'low'
            risk_factors = []
            
            if days_until_opening and days_until_opening < 7 and completion_rate < 80:
                risk_level = 'high'
                risk_factors.append('Opening in less than 7 days with <80% completion')
            elif overdue_tasks > 5:
                risk_level = 'high' if risk_level != 'high' else risk_level
                risk_factors.append(f'{overdue_tasks} overdue tasks')
            elif completion_rate < 50 and days_until_opening and days_until_opening < 30:
                risk_level = 'medium'
                risk_factors.append('Low completion rate with upcoming deadline')
            
            # Generate recommendations
            recommendations = []
            if overdue_tasks > 0:
                recommendations.append(f'Prioritize {overdue_tasks} overdue tasks immediately')
            if completion_rate < 60 and days_until_opening and days_until_opening < 14:
                recommendations.append('Consider extending opening date or adding resources')
            if risk_level == 'high':
                recommendations.append('Schedule immediate team meeting to address delays')
            
            insights.append({
                'store_id': store.id,
                'store_name': store.name,
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendations': recommendations,
                'metrics': {
                    'completion_rate': round(completion_rate, 1),
                    'overdue_tasks': overdue_tasks,
                    'days_until_opening': days_until_opening
                }
            })
        
        return jsonify({
            'insights': insights,
            'generated_at': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/predict/completion-date/<int:store_id>', methods=['GET'])
def predict_completion_date(store_id):
    """Predict likely completion date based on current progress"""
    try:
        store = Store.query.get_or_404(store_id)
        
        # Get task completion history (last 14 days)
        two_weeks_ago = datetime.utcnow() - timedelta(days=14)
        
        completed_recently = []
        for checklist in store.checklists:
            for task in checklist.tasks:
                if task.completed_at and task.completed_at >= two_weeks_ago:
                    completed_recently.append(task)
        
        # Calculate average tasks per day
        tasks_per_day = len(completed_recently) / 14 if len(completed_recently) > 0 else 0
        
        # Get remaining tasks
        remaining_tasks = sum(
            len([t for t in checklist.tasks if t.status != 'completed'])
            for checklist in store.checklists
        )
        
        # Predict completion
        if tasks_per_day > 0:
            days_to_complete = remaining_tasks / tasks_per_day
            predicted_completion = datetime.utcnow() + timedelta(days=days_to_complete)
        else:
            predicted_completion = None
        
        # Compare with opening date
        on_track = False
        days_difference = None
        if predicted_completion and store.opening_date:
            days_difference = (store.opening_date - predicted_completion).days
            on_track = days_difference >= 0
        
        return jsonify({
            'store_id': store_id,
            'store_name': store.name,
            'opening_date': store.opening_date.isoformat() if store.opening_date else None,
            'predicted_completion': predicted_completion.isoformat() if predicted_completion else None,
            'on_track': on_track,
            'days_difference': days_difference,
            'metrics': {
                'remaining_tasks': remaining_tasks,
                'average_tasks_per_day': round(tasks_per_day, 2),
                'tasks_completed_last_14_days': len(completed_recently)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
