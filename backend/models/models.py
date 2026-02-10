from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Import db from database module
from backend.database import db

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)  # Increased for bcrypt
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(50), default='team_member')  # admin, manager, team_member
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    requires_password_change = db.Column(db.Boolean, default=True)  # Force password change on first login
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the password matches"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Store(db.Model):
    """Store opening project model"""
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    opening_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='planning')  # planning, in_progress, completed, delayed
    workflow_stage = db.Column(db.Integer, default=0)  # 0-7: 0=initial, 1=nearby_store_update, 2=checklist_complete, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team_members = db.relationship('TeamMember', backref='store', lazy=True, cascade='all, delete-orphan')
    checklists = db.relationship('Checklist', backref='store', lazy=True, cascade='all, delete-orphan')
    whatsapp_group = db.relationship('WhatsAppGroup', backref='store', uselist=False, cascade='all, delete-orphan')
    nearby_store = db.relationship('NearbyStoreDetails', backref='store', uselist=False, cascade='all, delete-orphan')
    material_tracking = db.relationship('MaterialTracking', backref='store', uselist=False, cascade='all, delete-orphan')
    teamviewer_session = db.relationship('TeamViewerSession', backref='store', uselist=False, cascade='all, delete-orphan')
    workflow_stages = db.relationship('WorkflowStage', backref='store', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'opening_date': self.opening_date.isoformat() if self.opening_date else None,
            'status': self.status,
            'workflow_stage': self.workflow_stage,
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


class NearbyStoreDetails(db.Model):
    """Nearby store details for material shipment"""
    __tablename__ = 'nearby_store_details'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False, unique=True)
    store_name = db.Column(db.String(200), nullable=False)
    store_address = db.Column(db.Text)
    contact_person_name = db.Column(db.String(100), nullable=False)
    contact_person_mobile = db.Column(db.String(20), nullable=False)
    distance_km = db.Column(db.Float)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'store_name': self.store_name,
            'store_address': self.store_address,
            'contact_person_name': self.contact_person_name,
            'contact_person_mobile': self.contact_person_mobile,
            'distance_km': self.distance_km,
            'updated_by_id': self.updated_by_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MaterialTracking(db.Model):
    """Material tracking from warehouse to store"""
    __tablename__ = 'material_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False, unique=True)
    warehouse_sent_at = db.Column(db.DateTime)
    warehouse_sent_by_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    nearby_store_received_at = db.Column(db.DateTime)
    nearby_store_confirmed_by_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    store_sent_from_nearby_at = db.Column(db.DateTime)
    store_received_at = db.Column(db.DateTime)
    store_confirmed_by_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    current_location = db.Column(db.String(50), default='warehouse')  # warehouse, nearby_store, in_transit, store
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'warehouse_sent_at': self.warehouse_sent_at.isoformat() if self.warehouse_sent_at else None,
            'warehouse_sent_by_id': self.warehouse_sent_by_id,
            'nearby_store_received_at': self.nearby_store_received_at.isoformat() if self.nearby_store_received_at else None,
            'nearby_store_confirmed_by_id': self.nearby_store_confirmed_by_id,
            'store_sent_from_nearby_at': self.store_sent_from_nearby_at.isoformat() if self.store_sent_from_nearby_at else None,
            'store_received_at': self.store_received_at.isoformat() if self.store_received_at else None,
            'store_confirmed_by_id': self.store_confirmed_by_id,
            'current_location': self.current_location,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TeamViewerSession(db.Model):
    """TeamViewer session for installation support"""
    __tablename__ = 'teamviewer_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False, unique=True)
    teamviewer_id = db.Column(db.String(50), nullable=False)
    installation_started_at = db.Column(db.DateTime)
    installation_completed_at = db.Column(db.DateTime)
    technician_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    support_notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'teamviewer_id': self.teamviewer_id,
            'installation_started_at': self.installation_started_at.isoformat() if self.installation_started_at else None,
            'installation_completed_at': self.installation_completed_at.isoformat() if self.installation_completed_at else None,
            'technician_id': self.technician_id,
            'support_notes': self.support_notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class WorkflowStage(db.Model):
    """Workflow stage tracking for store opening process"""
    __tablename__ = 'workflow_stages'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    stage_number = db.Column(db.Integer, nullable=False)  # 1-7
    stage_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed, delayed, blocked
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    due_date = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assigned_to = db.relationship('TeamMember', foreign_keys=[assigned_to_id])
    escalations = db.relationship('EscalationHistory', backref='workflow_stage', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'stage_number': self.stage_number,
            'stage_name': self.stage_name,
            'status': self.status,
            'assigned_to_id': self.assigned_to_id,
            'assigned_to_name': self.assigned_to.name if self.assigned_to else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class EscalationHistory(db.Model):
    """Escalation history for workflow delays"""
    __tablename__ = 'escalation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_stage_id = db.Column(db.Integer, db.ForeignKey('workflow_stages.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    escalation_level = db.Column(db.Integer, nullable=False)  # 1=whatsapp, 2=sms, 3=call, 4=email_manager
    escalation_type = db.Column(db.String(50), nullable=False)  # whatsapp, sms, call, email
    recipient_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    recipient_phone = db.Column(db.String(20))
    recipient_email = db.Column(db.String(120))
    message = db.Column(db.Text)
    status = db.Column(db.String(50), default='sent')  # sent, failed, acknowledged
    response_received_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_stage_id': self.workflow_stage_id,
            'task_id': self.task_id,
            'escalation_level': self.escalation_level,
            'escalation_type': self.escalation_type,
            'recipient_id': self.recipient_id,
            'recipient_phone': self.recipient_phone,
            'recipient_email': self.recipient_email,
            'message': self.message,
            'status': self.status,
            'response_received_at': self.response_received_at.isoformat() if self.response_received_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
