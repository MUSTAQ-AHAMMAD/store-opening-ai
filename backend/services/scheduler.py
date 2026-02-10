from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class FollowUpScheduler:
    """Scheduler for automated follow-up messages"""
    
    def __init__(self, app=None):
        self.scheduler = BackgroundScheduler()
        self.app = app
        
        # Check if scheduler should be enabled
        self.enabled = os.getenv('ENABLE_SCHEDULER', 'true').lower() == 'true'
        
        if self.enabled:
            self._setup_jobs()
    
    def _setup_jobs(self):
        """Setup scheduled jobs"""
        # Check for follow-ups every hour
        self.scheduler.add_job(
            self.check_follow_ups,
            trigger=CronTrigger(minute=0),  # Run every hour at the top of the hour
            id='check_follow_ups',
            name='Check and send follow-up messages',
            replace_existing=True
        )
        
        # Check for overdue tasks every 6 hours
        self.scheduler.add_job(
            self.check_overdue_tasks,
            trigger=CronTrigger(hour='*/6'),  # Run every 6 hours
            id='check_overdue_tasks',
            name='Check for overdue tasks',
            replace_existing=True
        )
        
        # Daily summary at 9 AM
        self.scheduler.add_job(
            self.send_daily_summary,
            trigger=CronTrigger(hour=9, minute=0),  # Run at 9 AM daily
            id='daily_summary',
            name='Send daily summary',
            replace_existing=True
        )
    
    def start(self):
        """Start the scheduler"""
        if self.enabled and not self.scheduler.running:
            self.scheduler.start()
            print("Follow-up scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("Follow-up scheduler stopped")
    
    def check_follow_ups(self):
        """Check and send pending follow-up messages"""
        if not self.app:
            return
        
        with self.app.app_context():
            from app import db
            from backend.models.models import FollowUp, Task
            from backend.services.whatsapp_service import WhatsAppService
            
            # Get pending follow-ups that are due
            now = datetime.utcnow()
            pending_follow_ups = FollowUp.query.filter(
                FollowUp.status == 'pending',
                FollowUp.scheduled_time <= now
            ).all()
            
            whatsapp_service = WhatsAppService()
            
            for follow_up in pending_follow_ups:
                task = follow_up.task
                if task.assigned_to and task.assigned_to.phone:
                    # Send follow-up message
                    result = whatsapp_service.send_follow_up(task, task.assigned_to)
                    
                    if result.get('success'):
                        follow_up.status = 'sent'
                        follow_up.sent_at = datetime.utcnow()
                    else:
                        follow_up.status = 'failed'
                    
                    db.session.commit()
            
            print(f"Processed {len(pending_follow_ups)} follow-ups")
    
    def check_overdue_tasks(self):
        """Check for overdue tasks and send escalations"""
        if not self.app:
            return
        
        with self.app.app_context():
            from app import db
            from backend.models.models import Task, FollowUp
            from backend.services.whatsapp_service import WhatsAppService
            
            # Get overdue tasks
            now = datetime.utcnow()
            overdue_tasks = Task.query.filter(
                Task.due_date < now,
                Task.status != 'completed'
            ).all()
            
            whatsapp_service = WhatsAppService()
            
            for task in overdue_tasks:
                if task.assigned_to and task.assigned_to.phone:
                    # Check how many days overdue
                    days_overdue = (now - task.due_date).days
                    
                    # Determine escalation level
                    if days_overdue >= 7:
                        escalation_level = 2  # Critical
                    elif days_overdue >= 3:
                        escalation_level = 1  # Urgent
                    else:
                        escalation_level = 0  # Normal reminder
                    
                    # Check if we already sent an escalation recently
                    recent_escalation = FollowUp.query.filter(
                        FollowUp.task_id == task.id,
                        FollowUp.escalation_level >= escalation_level,
                        FollowUp.sent_at >= now - timedelta(days=1)
                    ).first()
                    
                    if not recent_escalation:
                        # Send escalation
                        result = whatsapp_service.send_escalation(
                            task, task.assigned_to, escalation_level
                        )
                        
                        # Create follow-up record
                        follow_up = FollowUp(
                            task_id=task.id,
                            scheduled_time=now,
                            message=f"Escalation level {escalation_level}",
                            status='sent' if result.get('success') else 'failed',
                            sent_at=now if result.get('success') else None,
                            escalation_level=escalation_level
                        )
                        db.session.add(follow_up)
            
            db.session.commit()
            print(f"Processed {len(overdue_tasks)} overdue tasks")
    
    def send_daily_summary(self):
        """Send daily summary to store managers"""
        if not self.app:
            return
        
        with self.app.app_context():
            from app import db
            from backend.models.models import Store, Task
            from backend.services.whatsapp_service import WhatsAppService
            
            whatsapp_service = WhatsAppService()
            
            # Get all active stores
            stores = Store.query.filter(Store.status.in_(['planning', 'in_progress'])).all()
            
            for store in stores:
                # Calculate statistics
                total_tasks = sum(len(checklist.tasks) for checklist in store.checklists)
                completed_tasks = sum(
                    len([task for task in checklist.tasks if task.status == 'completed'])
                    for checklist in store.checklists
                )
                pending_tasks = total_tasks - completed_tasks
                overdue_tasks = sum(
                    len([task for task in checklist.tasks 
                         if task.due_date and task.due_date < datetime.utcnow() and task.status != 'completed'])
                    for checklist in store.checklists
                )
                
                # Create summary message
                days_until_opening = (store.opening_date - datetime.utcnow()).days if store.opening_date else None
                
                summary = f"""
📊 Daily Summary - {store.name}

Opening Date: {store.opening_date.strftime('%Y-%m-%d') if store.opening_date else 'TBD'}
Days Until Opening: {days_until_opening if days_until_opening is not None else 'TBD'}

📋 Tasks Overview:
✅ Completed: {completed_tasks}/{total_tasks}
⏳ Pending: {pending_tasks}
⚠️ Overdue: {overdue_tasks}

Completion: {(completed_tasks/total_tasks*100) if total_tasks > 0 else 0:.1f}%
                """.strip()
                
                # Send to all active team members
                for member in store.team_members:
                    if member.is_active and member.phone:
                        whatsapp_service.send_message(member.phone, summary)
            
            print(f"Sent daily summaries for {len(stores)} stores")

# Global scheduler instance
scheduler = None

def init_scheduler(app):
    """Initialize the scheduler with the Flask app"""
    global scheduler
    scheduler = FollowUpScheduler(app)
    scheduler.start()
    return scheduler
