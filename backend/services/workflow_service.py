"""
Workflow Service for Store Opening Process
Manages the 7-stage workflow for store opening automation
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from backend.database import db
from backend.models.models import (
    Store, WorkflowStage, NearbyStoreDetails, MaterialTracking,
    TeamViewerSession, EscalationHistory, TeamMember, WhatsAppGroup
)
from backend.services.whatsapp_service import WhatsAppService
from backend.services.ai_service import get_ai_service
import logging

logger = logging.getLogger(__name__)

# Define the 7 workflow stages
WORKFLOW_STAGES = {
    1: {
        'name': 'Update Nearby Store Details',
        'description': 'Team member updates nearby store details with contact person and mobile',
        'days_before_opening': 20
    },
    2: {
        'name': 'Complete Checklist & Send to Warehouse',
        'description': 'Team completes checklist and sends to warehouse',
        'days_before_opening': 18
    },
    3: {
        'name': 'Confirm Material Reached Nearby Store',
        'description': 'Confirm material reached nearby store from warehouse',
        'days_before_opening': 15
    },
    4: {
        'name': 'Confirm Material Sent to Store',
        'description': 'Confirm material sent from nearby store to actual store',
        'days_before_opening': 12
    },
    5: {
        'name': 'Start Installation & Update TeamViewer ID',
        'description': 'Start installation process 1 day before or on opening day and update TeamViewer ID',
        'days_before_opening': 1
    },
    6: {
        'name': 'Final Checklist on Opening Day',
        'description': 'Complete final checklist verification on store opening day',
        'days_before_opening': 0
    },
    7: {
        'name': 'Store Opening Complete',
        'description': 'Store opening completed successfully',
        'days_before_opening': 0
    }
}


class WorkflowService:
    """Service for managing store opening workflow"""
    
    def __init__(self):
        self.whatsapp_service = WhatsAppService()
        self.ai_service = get_ai_service()
    
    def initialize_workflow(self, store: Store) -> List[WorkflowStage]:
        """Initialize workflow stages for a new store"""
        stages = []
        opening_date = store.opening_date
        
        for stage_num, stage_info in WORKFLOW_STAGES.items():
            due_date = opening_date - timedelta(days=stage_info['days_before_opening'])
            
            stage = WorkflowStage(
                store_id=store.id,
                stage_number=stage_num,
                stage_name=stage_info['name'],
                status='pending' if stage_num == 1 else 'pending',
                due_date=due_date
            )
            db.session.add(stage)
            stages.append(stage)
        
        # Set first stage to in_progress
        if stages:
            stages[0].status = 'in_progress'
            stages[0].started_at = datetime.utcnow()
        
        db.session.commit()
        logger.info(f"Initialized {len(stages)} workflow stages for store {store.id}")
        
        return stages
    
    def recalculate_timelines(self, store: Store, new_opening_date: datetime) -> bool:
        """Recalculate all stage timelines when opening date changes"""
        try:
            old_opening_date = store.opening_date
            store.opening_date = new_opening_date
            
            # Update all workflow stage due dates
            for stage in store.workflow_stages:
                if stage.status not in ['completed']:
                    stage_info = WORKFLOW_STAGES.get(stage.stage_number)
                    if stage_info:
                        stage.due_date = new_opening_date - timedelta(days=stage_info['days_before_opening'])
            
            db.session.commit()
            
            # Notify team via WhatsApp
            message = f"""🔔 Opening Date Updated - {store.name}

Previous Opening Date: {old_opening_date.strftime('%Y-%m-%d')}
New Opening Date: {new_opening_date.strftime('%Y-%m-%d')}

⚠️ All workflow stage timelines have been automatically recalculated.

Updated Stage Deadlines:
"""
            for stage in sorted(store.workflow_stages, key=lambda s: s.stage_number):
                if stage.status != 'completed':
                    message += f"\n{stage.stage_number}. {stage.stage_name}\n   Due: {stage.due_date.strftime('%Y-%m-%d')}"
            
            self._broadcast_to_team(store, message)
            
            logger.info(f"Recalculated timelines for store {store.id}: {old_opening_date} → {new_opening_date}")
            return True
            
        except Exception as e:
            logger.error(f"Error recalculating timelines: {e}")
            db.session.rollback()
            return False
    
    def advance_stage(self, store: Store, stage_number: int, completed_by: Optional[TeamMember] = None, notes: str = "") -> bool:
        """Advance workflow to next stage"""
        try:
            current_stage = WorkflowStage.query.filter_by(
                store_id=store.id,
                stage_number=stage_number
            ).first()
            
            if not current_stage:
                logger.error(f"Stage {stage_number} not found for store {store.id}")
                return False
            
            # Mark current stage as completed
            current_stage.status = 'completed'
            current_stage.completed_at = datetime.utcnow()
            if notes:
                current_stage.notes = notes
            
            # Update store workflow stage
            store.workflow_stage = stage_number
            
            # Start next stage
            next_stage = WorkflowStage.query.filter_by(
                store_id=store.id,
                stage_number=stage_number + 1
            ).first()
            
            if next_stage:
                next_stage.status = 'in_progress'
                next_stage.started_at = datetime.utcnow()
            
            db.session.commit()
            
            # Send notifications
            self._send_stage_completion_notification(store, current_stage, completed_by)
            if next_stage:
                self._send_stage_start_notification(store, next_stage)
            
            logger.info(f"Advanced store {store.id} from stage {stage_number} to {stage_number + 1}")
            return True
            
        except Exception as e:
            logger.error(f"Error advancing stage: {e}")
            db.session.rollback()
            return False
    
    def update_nearby_store_details(self, store: Store, details: Dict, updated_by: TeamMember) -> bool:
        """Handle Stage 1: Update nearby store details"""
        try:
            nearby_store = NearbyStoreDetails.query.filter_by(store_id=store.id).first()
            
            if not nearby_store:
                nearby_store = NearbyStoreDetails(store_id=store.id)
                db.session.add(nearby_store)
            
            nearby_store.store_name = details.get('store_name')
            nearby_store.store_address = details.get('store_address')
            nearby_store.contact_person_name = details.get('contact_person_name')
            nearby_store.contact_person_mobile = details.get('contact_person_mobile')
            nearby_store.distance_km = details.get('distance_km')
            nearby_store.updated_by_id = updated_by.id
            
            db.session.commit()
            
            # Advance to next stage
            self.advance_stage(store, 1, updated_by, f"Nearby store: {nearby_store.store_name}")
            
            logger.info(f"Updated nearby store details for store {store.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating nearby store details: {e}")
            db.session.rollback()
            return False
    
    def confirm_warehouse_shipment(self, store: Store, confirmed_by: TeamMember) -> bool:
        """Handle Stage 2: Confirm checklist complete and sent to warehouse"""
        try:
            material_tracking = MaterialTracking.query.filter_by(store_id=store.id).first()
            
            if not material_tracking:
                material_tracking = MaterialTracking(store_id=store.id)
                db.session.add(material_tracking)
            
            material_tracking.warehouse_sent_at = datetime.utcnow()
            material_tracking.warehouse_sent_by_id = confirmed_by.id
            material_tracking.current_location = 'in_transit'
            
            db.session.commit()
            
            # Notify the person who gave nearby store details
            self._notify_material_status(store, 'warehouse_sent', confirmed_by)
            
            # Advance to next stage
            self.advance_stage(store, 2, confirmed_by, "Material sent from warehouse")
            
            logger.info(f"Confirmed warehouse shipment for store {store.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error confirming warehouse shipment: {e}")
            db.session.rollback()
            return False
    
    def confirm_nearby_store_receipt(self, store: Store, confirmed_by: TeamMember) -> bool:
        """Handle Stage 3: Confirm material reached nearby store"""
        try:
            material_tracking = MaterialTracking.query.filter_by(store_id=store.id).first()
            
            if not material_tracking:
                logger.error(f"Material tracking not found for store {store.id}")
                return False
            
            material_tracking.nearby_store_received_at = datetime.utcnow()
            material_tracking.nearby_store_confirmed_by_id = confirmed_by.id
            material_tracking.current_location = 'nearby_store'
            
            db.session.commit()
            
            # Advance to next stage
            self.advance_stage(store, 3, confirmed_by, "Material confirmed at nearby store")
            
            logger.info(f"Confirmed nearby store receipt for store {store.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error confirming nearby store receipt: {e}")
            db.session.rollback()
            return False
    
    def confirm_store_receipt(self, store: Store, confirmed_by: TeamMember) -> bool:
        """Handle Stage 4: Confirm material reached the actual store"""
        try:
            material_tracking = MaterialTracking.query.filter_by(store_id=store.id).first()
            
            if not material_tracking:
                logger.error(f"Material tracking not found for store {store.id}")
                return False
            
            material_tracking.store_sent_from_nearby_at = datetime.utcnow()
            material_tracking.store_received_at = datetime.utcnow()
            material_tracking.store_confirmed_by_id = confirmed_by.id
            material_tracking.current_location = 'store'
            
            db.session.commit()
            
            # Advance to next stage
            self.advance_stage(store, 4, confirmed_by, "Material confirmed at store")
            
            logger.info(f"Confirmed store receipt for store {store.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error confirming store receipt: {e}")
            db.session.rollback()
            return False
    
    def start_installation(self, store: Store, teamviewer_id: str, technician: TeamMember) -> bool:
        """Handle Stage 5: Start installation and update TeamViewer ID"""
        try:
            teamviewer_session = TeamViewerSession.query.filter_by(store_id=store.id).first()
            
            if not teamviewer_session:
                teamviewer_session = TeamViewerSession(store_id=store.id)
                db.session.add(teamviewer_session)
            
            teamviewer_session.teamviewer_id = teamviewer_id
            teamviewer_session.installation_started_at = datetime.utcnow()
            teamviewer_session.technician_id = technician.id
            teamviewer_session.is_active = True
            
            db.session.commit()
            
            # Advance to next stage
            self.advance_stage(store, 5, technician, f"Installation started - TeamViewer ID: {teamviewer_id}")
            
            logger.info(f"Started installation for store {store.id} with TeamViewer ID: {teamviewer_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting installation: {e}")
            db.session.rollback()
            return False
    
    def complete_final_checklist(self, store: Store, completed_by: TeamMember) -> bool:
        """Handle Stage 6: Complete final checklist on opening day"""
        try:
            # Mark installation as complete
            teamviewer_session = TeamViewerSession.query.filter_by(store_id=store.id).first()
            if teamviewer_session:
                teamviewer_session.installation_completed_at = datetime.utcnow()
                teamviewer_session.is_active = False
            
            # Advance to next stage
            self.advance_stage(store, 6, completed_by, "Final checklist completed")
            
            logger.info(f"Completed final checklist for store {store.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error completing final checklist: {e}")
            db.session.rollback()
            return False
    
    def complete_store_opening(self, store: Store) -> bool:
        """Handle Stage 7: Mark store opening as complete"""
        try:
            store.status = 'completed'
            store.workflow_stage = 7
            
            # Complete final stage
            final_stage = WorkflowStage.query.filter_by(
                store_id=store.id,
                stage_number=7
            ).first()
            
            if final_stage:
                final_stage.status = 'completed'
                final_stage.completed_at = datetime.utcnow()
            
            db.session.commit()
            
            # Send completion notification
            self._send_completion_notification(store)
            
            logger.info(f"Completed store opening for store {store.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error completing store opening: {e}")
            db.session.rollback()
            return False
    
    def check_stage_delays(self, store: Store) -> List[WorkflowStage]:
        """Check for delayed workflow stages"""
        now = datetime.utcnow()
        delayed_stages = []
        
        for stage in store.workflow_stages:
            if stage.status not in ['completed'] and stage.due_date and stage.due_date < now:
                delayed_stages.append(stage)
        
        return delayed_stages
    
    def escalate_delayed_stage(self, stage: WorkflowStage, escalation_level: int) -> bool:
        """Escalate a delayed workflow stage"""
        try:
            store = Store.query.get(stage.store_id)
            if not store:
                return False
            
            # Find manager for escalation
            manager = TeamMember.query.filter_by(
                store_id=store.id,
                role='manager'
            ).first()
            
            if not manager:
                logger.warning(f"No manager found for store {store.id}")
                return False
            
            # Create escalation record
            escalation = EscalationHistory(
                workflow_stage_id=stage.id,
                escalation_level=escalation_level,
                escalation_type='email' if escalation_level >= 3 else 'whatsapp',
                recipient_id=manager.id,
                recipient_phone=manager.phone,
                recipient_email=manager.email,
                message=self._generate_escalation_message(store, stage, escalation_level),
                status='sent'
            )
            db.session.add(escalation)
            db.session.commit()
            
            # Send escalation notification
            self._send_escalation(manager, escalation.message, escalation_level)
            
            logger.info(f"Escalated stage {stage.id} at level {escalation_level}")
            return True
            
        except Exception as e:
            logger.error(f"Error escalating stage: {e}")
            db.session.rollback()
            return False
    
    def _send_stage_completion_notification(self, store: Store, stage: WorkflowStage, completed_by: Optional[TeamMember]):
        """Send notification when a stage is completed"""
        message = f"""✅ Stage {stage.stage_number} Completed - {store.name}

Stage: {stage.stage_name}
Completed by: {completed_by.name if completed_by else 'System'}
Completed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}

{stage.notes if stage.notes else ''}
"""
        self._broadcast_to_team(store, message)
    
    def _send_stage_start_notification(self, store: Store, stage: WorkflowStage):
        """Send notification when a new stage starts"""
        message = f"""🚀 New Stage Started - {store.name}

Stage {stage.stage_number}: {stage.stage_name}
Due Date: {stage.due_date.strftime('%Y-%m-%d') if stage.due_date else 'TBD'}

Please ensure this stage is completed on time.
"""
        self._broadcast_to_team(store, message)
    
    def _send_completion_notification(self, store: Store):
        """Send notification when store opening is complete"""
        message = f"""🎉 Store Opening Complete! - {store.name}

Congratulations to the entire team!

All workflow stages have been completed successfully.
Store opened on: {store.opening_date.strftime('%Y-%m-%d')}

Thank you for your hard work and dedication! 🙏
"""
        self._broadcast_to_team(store, message)
    
    def _notify_material_status(self, store: Store, status: str, notified_by: TeamMember):
        """Notify about material tracking status"""
        nearby_store = NearbyStoreDetails.query.filter_by(store_id=store.id).first()
        
        if not nearby_store:
            return
        
        # Find the person who updated nearby store details
        updater = TeamMember.query.get(nearby_store.updated_by_id)
        if not updater:
            return
        
        status_messages = {
            'warehouse_sent': f"Material has been sent from warehouse to nearby store: {nearby_store.store_name}",
            'nearby_received': f"Material has been received at nearby store: {nearby_store.store_name}",
            'store_sent': f"Material has been sent from nearby store to: {store.name}",
            'store_received': f"Material has been received at store: {store.name}"
        }
        
        message = f"""📦 Material Tracking Update - {store.name}

{status_messages.get(status, 'Status update')}

Contact Person: {nearby_store.contact_person_name}
Mobile: {nearby_store.contact_person_mobile}
"""
        
        self.whatsapp_service.send_message(updater.phone, message)
    
    def _generate_escalation_message(self, store: Store, stage: WorkflowStage, level: int) -> str:
        """Generate escalation message using AI if available"""
        days_overdue = (datetime.utcnow() - stage.due_date).days if stage.due_date else 0
        
        if self.ai_service.enabled:
            context = {
                'days_overdue': days_overdue,
                'stage_name': stage.stage_name,
                'store_name': store.name,
                'opening_date': store.opening_date.strftime('%Y-%m-%d'),
                'escalation_level': level
            }
            
            return self.ai_service.generate_escalation_message(
                {'title': stage.stage_name},
                {'name': 'Manager', 'role': 'manager'},
                level,
                context
            )
        else:
            urgency = ['⚠️ REMINDER', '🚨 URGENT', '🔴 CRITICAL', '❌ EMERGENCY'][min(level - 1, 3)]
            return f"""{urgency} - Workflow Stage Delayed

Store: {store.name}
Stage {stage.stage_number}: {stage.stage_name}
Days Overdue: {days_overdue}
Opening Date: {store.opening_date.strftime('%Y-%m-%d')}

This stage is significantly delayed. Immediate action required!
"""
    
    def _send_escalation(self, recipient: TeamMember, message: str, level: int):
        """Send escalation through appropriate channel"""
        # Always send WhatsApp
        self.whatsapp_service.send_message(recipient.phone, message)
        
        # For high levels, also send via other channels (email, SMS, call)
        # This would integrate with email_service and voice_service
        # Implementation depends on available services
    
    def _broadcast_to_team(self, store: Store, message: str):
        """Broadcast message to all team members via WhatsApp group"""
        whatsapp_group = WhatsAppGroup.query.filter_by(store_id=store.id).first()
        
        if whatsapp_group and whatsapp_group.is_active:
            self.whatsapp_service.send_message_to_group(
                whatsapp_group,
                message,
                store.team_members
            )
        else:
            # Send individually if no group
            for member in store.team_members:
                if member.is_active and member.phone:
                    self.whatsapp_service.send_message(member.phone, message)


# Global workflow service instance
workflow_service = None

def get_workflow_service():
    """Get or create workflow service instance"""
    global workflow_service
    if workflow_service is None:
        workflow_service = WorkflowService()
    return workflow_service
