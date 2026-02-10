from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.models import Store, Task, Checklist
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard analytics"""
    
    # Get all stores
    total_stores = Store.query.count()
    active_stores = Store.query.filter(Store.status.in_(['planning', 'in_progress'])).count()
    completed_stores = Store.query.filter_by(status='completed').count()
    
    # Get all tasks
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    pending_tasks = Task.query.filter(Task.status != 'completed').count()
    overdue_tasks = Task.query.filter(
        Task.due_date < datetime.utcnow(),
        Task.status != 'completed'
    ).count()
    
    # Get tasks by priority
    high_priority = Task.query.filter_by(priority='high', status='pending').count()
    critical_priority = Task.query.filter_by(priority='critical', status='pending').count()
    
    # Get upcoming openings (next 30 days)
    upcoming_openings = Store.query.filter(
        Store.opening_date >= datetime.utcnow(),
        Store.opening_date <= datetime.utcnow() + timedelta(days=30)
    ).all()
    
    # Store completion rates
    stores = Store.query.all()
    store_stats = []
    for store in stores:
        total = sum(len(checklist.tasks) for checklist in store.checklists)
        completed = sum(
            len([task for task in checklist.tasks if task.status == 'completed'])
            for checklist in store.checklists
        )
        store_stats.append({
            'id': store.id,
            'name': store.name,
            'opening_date': store.opening_date.isoformat() if store.opening_date else None,
            'status': store.status,
            'total_tasks': total,
            'completed_tasks': completed,
            'completion_percentage': (completed / total * 100) if total > 0 else 0
        })
    
    return jsonify({
        'summary': {
            'total_stores': total_stores,
            'active_stores': active_stores,
            'completed_stores': completed_stores,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'high_priority_tasks': high_priority,
            'critical_priority_tasks': critical_priority
        },
        'upcoming_openings': [
            {
                'id': store.id,
                'name': store.name,
                'location': store.location,
                'opening_date': store.opening_date.isoformat() if store.opening_date else None,
                'days_until_opening': (store.opening_date - datetime.utcnow()).days if store.opening_date else None
            }
            for store in upcoming_openings
        ],
        'stores': store_stats
    }), 200

@bp.route('/store/<int:store_id>/progress', methods=['GET'])
def get_store_progress(store_id):
    """Get detailed progress for a store"""
    store = Store.query.get_or_404(store_id)
    
    # Get tasks by status
    tasks_by_status = {}
    tasks_by_priority = {}
    tasks_by_category = {}
    
    for checklist in store.checklists:
        for task in checklist.tasks:
            # By status
            tasks_by_status[task.status] = tasks_by_status.get(task.status, 0) + 1
            
            # By priority
            tasks_by_priority[task.priority] = tasks_by_priority.get(task.priority, 0) + 1
            
            # By category
            category = checklist.category or 'other'
            tasks_by_category[category] = tasks_by_category.get(category, 0) + 1
    
    # Calculate daily progress (last 7 days)
    daily_progress = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        completed_on_day = Task.query.join(Checklist).filter(
            Checklist.store_id == store_id,
            Task.completed_at >= date_start,
            Task.completed_at <= date_end
        ).count()
        
        daily_progress.append({
            'date': date.strftime('%Y-%m-%d'),
            'completed_tasks': completed_on_day
        })
    
    return jsonify({
        'store': store.to_dict(),
        'tasks_by_status': tasks_by_status,
        'tasks_by_priority': tasks_by_priority,
        'tasks_by_category': tasks_by_category,
        'daily_progress': list(reversed(daily_progress))
    }), 200

@bp.route('/report', methods=['GET'])
def generate_report():
    """Generate comprehensive report"""
    store_id = request.args.get('store_id', type=int)
    
    if store_id:
        stores = [Store.query.get_or_404(store_id)]
    else:
        stores = Store.query.all()
    
    report = {
        'generated_at': datetime.utcnow().isoformat(),
        'stores': []
    }
    
    for store in stores:
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
        
        store_report = {
            'store': store.to_dict(),
            'statistics': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': total_tasks - completed_tasks,
                'overdue_tasks': overdue_tasks,
                'completion_percentage': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                'team_size': len(store.team_members)
            },
            'checklists': [
                {
                    'name': checklist.name,
                    'category': checklist.category,
                    'total_tasks': len(checklist.tasks),
                    'completed_tasks': len([task for task in checklist.tasks if task.status == 'completed'])
                }
                for checklist in store.checklists
            ]
        }
        report['stores'].append(store_report)
    
    return jsonify(report), 200
