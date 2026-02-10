from datetime import datetime
from app import db

class Store(db.Model):
    """Store opening project model"""
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    opening_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='planning')  # planning, in_progress, completed, delayed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team_members = db.relationship('TeamMember', backref='store', lazy=True, cascade='all, delete-orphan')
    checklists = db.relationship('Checklist', backref='store', lazy=True, cascade='all, delete-orphan')
    whatsapp_group = db.relationship('WhatsAppGroup', backref='store', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'opening_date': self.opening_date.isoformat() if self.opening_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TeamMember(db.Model):
    """Team member model for store openings"""
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='assigned_to', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'phone': self.phone,
            'email': self.email,
            'store_id': self.store_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Checklist(db.Model):
    """Checklist model for store opening items"""
    __tablename__ = 'checklists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    category = db.Column(db.String(50))  # hardware, software, accounts, setup
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='checklist', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'store_id': self.store_id,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'tasks': [task.to_dict() for task in self.tasks]
        }


class Task(db.Model):
    """Task model for checklist items"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklists.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed, blocked
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    follow_ups = db.relationship('FollowUp', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'checklist_id': self.checklist_id,
            'assigned_to_id': self.assigned_to_id,
            'assigned_to_name': self.assigned_to.name if self.assigned_to else None,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class WhatsAppGroup(db.Model):
    """WhatsApp group model for store communication"""
    __tablename__ = 'whatsapp_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False, unique=True)
    group_name = db.Column(db.String(200), nullable=False)
    group_id = db.Column(db.String(100))  # External WhatsApp group ID
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    archived_at = db.Column(db.DateTime)
    
    # Relationships
    archived_conversations = db.relationship('ArchivedConversation', backref='group', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'group_name': self.group_name,
            'group_id': self.group_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'archived_at': self.archived_at.isoformat() if self.archived_at else None
        }


class ArchivedConversation(db.Model):
    """Archived WhatsApp conversation data"""
    __tablename__ = 'archived_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('whatsapp_groups.id'), nullable=False)
    sender = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    message_type = db.Column(db.String(50), default='text')  # text, image, document, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'sender': self.sender,
            'message': self.message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'message_type': self.message_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class FollowUp(db.Model):
    """Follow-up reminder model"""
    __tablename__ = 'follow_ups'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, sent, acknowledged, failed
    sent_at = db.Column(db.DateTime)
    escalation_level = db.Column(db.Integer, default=0)  # 0=normal, 1=first escalation, 2=second, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'message': self.message,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'escalation_level': self.escalation_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
