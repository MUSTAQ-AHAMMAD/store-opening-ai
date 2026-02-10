"""
Beta testing data seed script
Generates sample data for testing the Store Opening AI system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from app import app
from backend.database import db
from backend.models.models import (
    Store, TeamMember, Checklist, Task, 
    WhatsAppGroup, ArchivedConversation, FollowUp
)
import random

def clear_data():
    """Clear all existing data"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database cleared and recreated")

def seed_stores():
    """Create 5 sample stores"""
    stores_data = [
        {
            'name': 'Downtown Tech Hub',
            'location': 'New York, NY',
            'opening_date': datetime.utcnow() + timedelta(days=15),
            'status': 'in_progress'
        },
        {
            'name': 'Westside Electronics',
            'location': 'Los Angeles, CA',
            'opening_date': datetime.utcnow() + timedelta(days=30),
            'status': 'planning'
        },
        {
            'name': 'Central Plaza Store',
            'location': 'Chicago, IL',
            'opening_date': datetime.utcnow() + timedelta(days=7),
            'status': 'in_progress'
        },
        {
            'name': 'Bay Area Outlet',
            'location': 'San Francisco, CA',
            'opening_date': datetime.utcnow() + timedelta(days=45),
            'status': 'planning'
        },
        {
            'name': 'Metro Center',
            'location': 'Boston, MA',
            'opening_date': datetime.utcnow() - timedelta(days=5),
            'status': 'completed'
        }
    ]
    
    stores = []
    for data in stores_data:
        store = Store(**data)
        db.session.add(store)
        stores.append(store)
    
    db.session.commit()
    print(f"Created {len(stores)} stores")
    return stores

def seed_team_members(stores):
    """Create 20+ team members across stores"""
    roles = ['Store Manager', 'IT Technician', 'Operations Lead', 'Training Coordinator', 'Logistics Manager']
    first_names = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Robert', 'Amanda', 'James', 'Lisa']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    team_members = []
    member_id = 1
    
    for store in stores:
        # Each store gets 4-6 team members
        num_members = random.randint(4, 6)
        
        for i in range(num_members):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            role = random.choice(roles)
            phone = f"+1555{member_id:07d}"
            email = f"{name.lower().replace(' ', '.')}@company.com"
            
            member = TeamMember(
                name=name,
                role=role,
                phone=phone,
                email=email,
                store_id=store.id,
                is_active=True
            )
            db.session.add(member)
            team_members.append(member)
            member_id += 1
    
    db.session.commit()
    print(f"Created {len(team_members)} team members")
    return team_members

def seed_checklists_and_tasks(stores, team_members):
    """Create checklists and tasks for each store"""
    
    checklist_templates = {
        'Hardware Setup': {
            'category': 'hardware',
            'tasks': [
                {'title': 'Install POS System', 'priority': 'critical', 'days_offset': -5},
                {'title': 'Setup Printers', 'priority': 'high', 'days_offset': -3},
                {'title': 'Configure Barcode Scanners', 'priority': 'high', 'days_offset': -3},
                {'title': 'Install Security Cameras', 'priority': 'medium', 'days_offset': -7},
                {'title': 'Setup Network Equipment', 'priority': 'critical', 'days_offset': -10},
            ]
        },
        'Software & Accounts': {
            'category': 'software',
            'tasks': [
                {'title': 'Create Employee Accounts', 'priority': 'high', 'days_offset': -4},
                {'title': 'Install Inventory Management Software', 'priority': 'critical', 'days_offset': -6},
                {'title': 'Configure POS Software', 'priority': 'critical', 'days_offset': -5},
                {'title': 'Setup Email Accounts', 'priority': 'medium', 'days_offset': -7},
                {'title': 'Install Antivirus Software', 'priority': 'high', 'days_offset': -8},
            ]
        },
        'Connectivity': {
            'category': 'setup',
            'tasks': [
                {'title': 'Activate Internet Connection', 'priority': 'critical', 'days_offset': -10},
                {'title': 'Install SIM Cards for Mobile Devices', 'priority': 'high', 'days_offset': -5},
                {'title': 'Setup WiFi Network', 'priority': 'high', 'days_offset': -8},
                {'title': 'Test Payment Gateway', 'priority': 'critical', 'days_offset': -3},
            ]
        },
        'Training & Documentation': {
            'category': 'accounts',
            'tasks': [
                {'title': 'Staff Training on POS', 'priority': 'high', 'days_offset': -2},
                {'title': 'Create Operation Manual', 'priority': 'medium', 'days_offset': -7},
                {'title': 'Security Protocol Training', 'priority': 'medium', 'days_offset': -4},
                {'title': 'Emergency Procedures Training', 'priority': 'high', 'days_offset': -3},
            ]
        }
    }
    
    all_tasks = []
    
    for store in stores:
        store_team = [m for m in team_members if m.store_id == store.id]
        
        for checklist_name, checklist_data in checklist_templates.items():
            checklist = Checklist(
                name=checklist_name,
                description=f"{checklist_name} checklist for {store.name}",
                store_id=store.id,
                category=checklist_data['category']
            )
            db.session.add(checklist)
            db.session.flush()  # Get checklist ID
            
            for task_data in checklist_data['tasks']:
                # Assign to random team member
                assigned_to = random.choice(store_team) if store_team else None
                
                # Calculate due date based on opening date
                due_date = store.opening_date + timedelta(days=task_data['days_offset'])
                
                # Determine status based on due date and store status
                if store.status == 'completed':
                    status = 'completed'
                    completed_at = due_date + timedelta(hours=random.randint(1, 48))
                elif due_date < datetime.utcnow():
                    # Overdue tasks - some completed, some not
                    if random.random() > 0.3:  # 70% completed
                        status = 'completed'
                        completed_at = due_date + timedelta(hours=random.randint(1, 48))
                    else:
                        status = random.choice(['pending', 'in_progress', 'blocked'])
                        completed_at = None
                else:
                    status = random.choice(['pending', 'in_progress'])
                    completed_at = None
                
                task = Task(
                    title=task_data['title'],
                    description=f"Complete {task_data['title']} for store opening",
                    checklist_id=checklist.id,
                    assigned_to_id=assigned_to.id if assigned_to else None,
                    status=status,
                    priority=task_data['priority'],
                    due_date=due_date,
                    completed_at=completed_at
                )
                db.session.add(task)
                all_tasks.append(task)
    
    db.session.commit()
    print(f"Created checklists and {len(all_tasks)} tasks")
    return all_tasks

def seed_whatsapp_groups(stores):
    """Create WhatsApp groups for stores"""
    groups = []
    
    for store in stores:
        group = WhatsAppGroup(
            store_id=store.id,
            group_name=f"{store.name} - Opening Team",
            group_id=f"group_{store.id}_simulation",
            is_active=store.status != 'completed',
            archived_at=datetime.utcnow() if store.status == 'completed' else None
        )
        db.session.add(group)
        groups.append(group)
    
    db.session.commit()
    print(f"Created {len(groups)} WhatsApp groups")
    return groups

def seed_archived_conversations(groups):
    """Create sample archived conversations"""
    
    sample_messages = [
        "Welcome to the team! Let's make this opening successful! 🎉",
        "POS system installation is scheduled for tomorrow",
        "Has anyone completed the network setup?",
        "Security cameras are installed and working",
        "We need to schedule staff training ASAP",
        "Great progress today team! Keep it up!",
        "Reminder: Internet activation is critical",
        "All printers are now configured",
        "Payment gateway testing completed successfully",
        "Store manager: Please update task statuses",
    ]
    
    conversations = []
    
    for group in groups:
        if group.archived_at:  # Only for archived groups
            # Create 20-30 messages per archived group
            num_messages = random.randint(20, 30)
            store_team = group.store.team_members
            
            for i in range(num_messages):
                sender = random.choice(store_team) if store_team else None
                
                conversation = ArchivedConversation(
                    group_id=group.id,
                    sender=sender.name if sender else "System",
                    message=random.choice(sample_messages),
                    timestamp=datetime.utcnow() - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23)),
                    message_type='text'
                )
                db.session.add(conversation)
                conversations.append(conversation)
    
    db.session.commit()
    print(f"Created {len(conversations)} archived conversations")
    return conversations

def seed_follow_ups(tasks):
    """Create follow-up reminders for tasks"""
    follow_ups = []
    
    for task in tasks:
        # Create follow-ups for pending/in_progress tasks
        if task.status in ['pending', 'in_progress'] and task.due_date:
            # Reminder 2 days before due date
            if task.due_date > datetime.utcnow():
                follow_up = FollowUp(
                    task_id=task.id,
                    scheduled_time=task.due_date - timedelta(days=2),
                    message=f"Reminder: {task.title} is due in 2 days",
                    status='pending' if task.due_date - timedelta(days=2) > datetime.utcnow() else 'sent',
                    sent_at=task.due_date - timedelta(days=2) if task.due_date - timedelta(days=2) <= datetime.utcnow() else None,
                    escalation_level=0
                )
                db.session.add(follow_up)
                follow_ups.append(follow_up)
            
            # Escalation for overdue tasks
            if task.due_date < datetime.utcnow():
                days_overdue = (datetime.utcnow() - task.due_date).days
                escalation_level = min(days_overdue // 3, 2)
                
                follow_up = FollowUp(
                    task_id=task.id,
                    scheduled_time=datetime.utcnow() - timedelta(days=1),
                    message=f"Escalation: {task.title} is overdue",
                    status='sent',
                    sent_at=datetime.utcnow() - timedelta(hours=random.randint(1, 24)),
                    escalation_level=escalation_level
                )
                db.session.add(follow_up)
                follow_ups.append(follow_up)
    
    db.session.commit()
    print(f"Created {len(follow_ups)} follow-ups")
    return follow_ups

def seed_all():
    """Seed all beta testing data"""
    print("\n" + "="*50)
    print("SEEDING BETA TESTING DATA")
    print("="*50 + "\n")
    
    with app.app_context():
        # Clear existing data
        clear_data()
        
        # Seed data in order
        stores = seed_stores()
        team_members = seed_team_members(stores)
        tasks = seed_checklists_and_tasks(stores, team_members)
        groups = seed_whatsapp_groups(stores)
        conversations = seed_archived_conversations(groups)
        follow_ups = seed_follow_ups(tasks)
        
        print("\n" + "="*50)
        print("SEEDING COMPLETE!")
        print("="*50)
        print(f"\nSummary:")
        print(f"  - Stores: {len(stores)}")
        print(f"  - Team Members: {len(team_members)}")
        print(f"  - Tasks: {len(tasks)}")
        print(f"  - WhatsApp Groups: {len(groups)}")
        print(f"  - Archived Conversations: {len(conversations)}")
        print(f"  - Follow-ups: {len(follow_ups)}")
        print("\nYou can now run the application and test with this data!")
        print()

if __name__ == '__main__':
    seed_all()
