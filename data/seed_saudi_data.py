"""
Saudi Arabia specific seed data for Store Opening AI
Generates sample data with Saudi locations, Arabic names, and local formats
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta, timezone
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
        # Drop all tables except User table to preserve logins
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            if table.name != 'user':
                db.session.execute(table.delete())
        db.session.commit()
        print("Database cleared (preserved users)")

def seed_stores():
    """Create 5 sample stores in Saudi Arabia"""
    stores_data = [
        {
            'name': 'Riyadh Tech Hub',
            'location': 'Riyadh, Saudi Arabia',
            'opening_date': datetime.now(timezone.utc) + timedelta(days=15),
            'status': 'in_progress'
        },
        {
            'name': 'Jeddah Electronics Center',
            'location': 'Jeddah, Saudi Arabia',
            'opening_date': datetime.now(timezone.utc) + timedelta(days=30),
            'status': 'planning'
        },
        {
            'name': 'Dammam Plaza Store',
            'location': 'Dammam, Saudi Arabia',
            'opening_date': datetime.now(timezone.utc) + timedelta(days=7),
            'status': 'in_progress'
        },
        {
            'name': 'Mecca Mall Outlet',
            'location': 'Mecca, Saudi Arabia',
            'opening_date': datetime.now(timezone.utc) + timedelta(days=45),
            'status': 'planning'
        },
        {
            'name': 'Medina Central Store',
            'location': 'Medina, Saudi Arabia',
            'opening_date': datetime.now(timezone.utc) - timedelta(days=5),
            'status': 'completed'
        }
    ]
    
    stores = []
    for data in stores_data:
        store = Store(**data)
        db.session.add(store)
        stores.append(store)
    
    db.session.commit()
    print(f"Created {len(stores)} stores in Saudi Arabia")
    return stores

def seed_team_members(stores):
    """Create 20+ team members with Saudi/Arabic names"""
    roles = ['Store Manager', 'IT Technician', 'Operations Lead', 'Training Coordinator', 'Logistics Manager']
    
    # Saudi/Arabic first names
    first_names = ['Ahmed', 'Mohammed', 'Fatima', 'Sarah', 'Abdullah', 'Nora', 'Omar', 'Maha', 'Khalid', 'Layla',
                   'Ali', 'Aisha', 'Hassan', 'Zainab', 'Fahad', 'Mariam', 'Tariq', 'Nouf', 'Youssef', 'Reem']
    
    # Saudi/Arabic last names
    last_names = ['Al-Saud', 'Al-Otaibi', 'Al-Ghamdi', 'Al-Zahrani', 'Al-Qahtani', 'Al-Harbi', 'Al-Mutairi', 
                  'Al-Malki', 'Al-Shammari', 'Al-Dosari', 'Al-Rashid', 'Al-Ahmed', 'Al-Mohammed']
    
    team_members = []
    member_id = 1
    
    for store in stores:
        # Each store gets 4-6 team members
        num_members = random.randint(4, 6)
        
        for i in range(num_members):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            role = random.choice(roles)
            # Saudi phone numbers format: +966 5X XXX XXXX
            phone = f"+9665{random.randint(0, 9)}{random.randint(1000000, 9999999)}"
            email = f"{name.lower().replace(' ', '.').replace('-', '')}@company.sa"
            
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
        
        # Make store.opening_date timezone-aware if it's naive (from database)
        store_opening_date = store.opening_date
        if store_opening_date.tzinfo is None:
            store_opening_date = store_opening_date.replace(tzinfo=timezone.utc)
        
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
                due_date = store_opening_date + timedelta(days=task_data['days_offset'])
                
                # Get current time - use timezone-aware for comparison
                now_utc = datetime.now(timezone.utc)
                
                # Determine status based on due date and store status
                if store.status == 'completed':
                    status = 'completed'
                    completed_at = due_date + timedelta(hours=random.randint(1, 48))
                elif due_date < now_utc:
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
            archived_at=datetime.now(timezone.utc) if store.status == 'completed' else None
        )
        db.session.add(group)
        groups.append(group)
    
    db.session.commit()
    print(f"Created {len(groups)} WhatsApp groups")
    return groups

def seed_archived_conversations(groups):
    """Create sample archived conversations in Arabic/English mix"""
    
    sample_messages = [
        "Welcome to the team! Let's make this opening successful! 🎉",
        "مرحبا بالجميع! نتمنى لكم التوفيق",
        "POS system installation is scheduled for tomorrow",
        "Has anyone completed the network setup?",
        "Security cameras are installed and working",
        "We need to schedule staff training ASAP",
        "Great progress today team! Keep it up!",
        "Reminder: Internet activation is critical",
        "تم إكمال تثبيت الطابعات",
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
                message = random.choice(sample_messages)
                
                # Create timestamp within last 30 days before archive
                days_ago = random.randint(1, 30)
                message_time = group.archived_at - timedelta(days=days_ago, hours=random.randint(0, 23))
                
                conv = ArchivedConversation(
                    group_id=group.id,
                    sender=sender.name if sender else "System",
                    message=message,
                    timestamp=message_time
                )
                db.session.add(conv)
                conversations.append(conv)
    
    db.session.commit()
    print(f"Created {len(conversations)} archived messages")
    return conversations

def seed_follow_ups(tasks, team_members):
    """Create follow-up reminders for tasks"""
    follow_ups = []
    
    # Get current time - use timezone-aware for comparison
    now_utc = datetime.now(timezone.utc)
    
    # Create follow-ups for overdue/upcoming tasks
    for task in tasks:
        if task.status in ['pending', 'in_progress', 'blocked']:
            # Make task.due_date timezone-aware if it's naive (from database)
            task_due_date = task.due_date
            if task_due_date.tzinfo is None:
                task_due_date = task_due_date.replace(tzinfo=timezone.utc)
            
            # Determine follow-up type
            if task_due_date < now_utc:
                # Overdue - create escalation
                days_overdue = (now_utc - task_due_date).days
                
                if days_overdue >= 7:
                    escalation_level = 2
                    message = f"CRITICAL: Task '{task.title}' is {days_overdue} days overdue. Immediate action required!"
                elif days_overdue >= 3:
                    escalation_level = 1
                    message = f"URGENT: Task '{task.title}' is {days_overdue} days overdue. Please complete ASAP."
                else:
                    escalation_level = 0
                    message = f"Reminder: Task '{task.title}' is {days_overdue} days overdue."
                
                scheduled_time = now_utc + timedelta(hours=random.randint(1, 6))
            else:
                # Upcoming - create reminder
                escalation_level = 0
                days_until_due = (task_due_date - now_utc).days
                message = f"Reminder: Task '{task.title}' is due in {days_until_due} days."
                scheduled_time = task_due_date - timedelta(days=1)
            
            # Only create follow-up for assigned tasks
            if task.assigned_to_id:
                follow_up = FollowUp(
                    task_id=task.id,
                    message=message,
                    scheduled_time=scheduled_time,
                    status='pending' if scheduled_time > now_utc else 'sent',
                    escalation_level=escalation_level,
                    sent_at=now_utc if scheduled_time <= now_utc else None
                )
                db.session.add(follow_up)
                follow_ups.append(follow_up)
    
    db.session.commit()
    print(f"Created {len(follow_ups)} follow-up reminders")
    return follow_ups

def run_seed():
    """Main function to seed all data"""
    with app.app_context():
        print("\n" + "="*60)
        print("SEEDING SAUDI ARABIA DATA")
        print("="*60 + "\n")
        
        # Clear existing data (except users)
        clear_data()
        
        # Seed data
        stores = seed_stores()
        team_members = seed_team_members(stores)
        tasks = seed_checklists_and_tasks(stores, team_members)
        groups = seed_whatsapp_groups(stores)
        conversations = seed_archived_conversations(groups)
        follow_ups = seed_follow_ups(tasks, team_members)
        
        print("\n" + "="*60)
        print("SEEDING COMPLETE!")
        print("="*60)
        print(f"✓ {len(stores)} stores created")
        print(f"✓ {len(team_members)} team members created")
        print(f"✓ {len(tasks)} tasks created")
        print(f"✓ {len(groups)} WhatsApp groups created")
        print(f"✓ {len(conversations)} archived messages created")
        print(f"✓ {len(follow_ups)} follow-up reminders created")
        print("\nAll data uses Saudi Arabia locations!")
        print("="*60 + "\n")

if __name__ == '__main__':
    run_seed()
