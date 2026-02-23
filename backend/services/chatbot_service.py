"""
Chatbot Service for WhatsApp Incoming Message Handling.

This service processes messages received via the Twilio WhatsApp webhook,
builds context from the database, generates an AI reply, and sends it back
to the sender through the WhatsApp service.
"""

import logging
import re
from datetime import datetime
from typing import Optional

from backend.database import db
from backend.models.models import (
    TeamMember, Store, Task, Checklist, WhatsAppGroup, ArchivedConversation
)
from backend.services.ai_service import get_ai_service
from backend.services.whatsapp_service import WhatsAppService

logger = logging.getLogger(__name__)


class ChatbotService:
    """Handle incoming WhatsApp messages and generate intelligent replies."""

    def __init__(self):
        self.ai_service = get_ai_service()
        self.whatsapp_service = WhatsAppService()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def handle_incoming_message(self, from_number: str, body: str) -> str:
        """
        Process an incoming WhatsApp message and return the reply text.

        Args:
            from_number: Sender's number, e.g. 'whatsapp:+1234567890'
            body: The text body of the incoming message

        Returns:
            str: The reply to send back to the sender
        """
        # Normalize the phone number (strip 'whatsapp:' prefix for DB lookup)
        bare_phone = from_number.replace('whatsapp:', '').strip()

        # Try to find the team member by phone
        member = TeamMember.query.filter_by(phone=bare_phone, is_active=True).first()

        # Archive the incoming message if we can associate it with a group
        self._archive_message(member, from_number, body)

        # Handle "done <task-id>" command before building full context
        done_match = re.match(r'^done\s+(\d+)$', body.strip(), re.IGNORECASE)
        if done_match and member:
            task_id = int(done_match.group(1))
            return self._handle_done_command(task_id, member)

        # Build context for AI / default response
        context = self._build_context(member)

        # Generate reply
        reply = self.ai_service.generate_chatbot_response(body, context)

        # Send the reply via WhatsApp
        self.whatsapp_service.send_message(from_number, reply)

        return reply

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_context(self, member: Optional[TeamMember]) -> dict:
        """Build the context dict passed to the AI service."""
        if not member:
            return {
                'member_name': 'Guest',
                'role': 'unknown',
                'pending_tasks': [],
                'store_name': 'N/A',
                'store_status': 'N/A',
                'days_until_opening': None
            }

        store: Optional[Store] = Store.query.get(member.store_id)

        # Collect pending/in-progress tasks for this member
        pending_tasks = []
        for checklist in (store.checklists if store else []):
            for task in checklist.tasks:
                if task.assigned_to_id == member.id and task.status not in ('completed',):
                    pending_tasks.append(task.to_dict())

        days_until_opening = None
        if store and store.opening_date:
            delta = (store.opening_date - datetime.utcnow()).days
            days_until_opening = max(delta, 0)

        return {
            'member_name': member.name,
            'role': member.role,
            'pending_tasks': pending_tasks,
            'store_name': store.name if store else 'N/A',
            'store_status': store.status if store else 'N/A',
            'days_until_opening': days_until_opening
        }

    def _handle_done_command(self, task_id: int, member: TeamMember) -> str:
        """Mark a task complete via 'done <task-id>' command."""
        task: Optional[Task] = Task.query.get(task_id)

        if not task:
            reply = f"❌ Task #{task_id} not found. Send *status* to see your task IDs."
        elif task.assigned_to_id != member.id:
            reply = f"⚠️ Task #{task_id} is not assigned to you."
        elif task.status == 'completed':
            reply = f"✅ Task #{task_id} is already marked as completed!"
        else:
            task.status = 'completed'
            task.completed_at = datetime.utcnow()
            try:
                db.session.commit()
                reply = (
                    f"✅ Task *{task.title}* marked as completed!\n\n"
                    "Great work! Send *status* to see your remaining tasks."
                )
                logger.info(f"Task {task_id} marked complete by {member.name} via WhatsApp")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error marking task {task_id} complete: {e}")
                reply = "⚠️ Could not update task status. Please try again or update via the dashboard."

        self.whatsapp_service.send_message(f'whatsapp:{member.phone}', reply)
        return reply

    def _archive_message(self, member: Optional[TeamMember], from_number: str, body: str):
        """Archive incoming message for audit trail."""
        try:
            if not member:
                return

            group = WhatsAppGroup.query.filter_by(
                store_id=member.store_id, is_active=True
            ).first()

            if not group:
                return

            archived = ArchivedConversation(
                group_id=group.id,
                sender=member.name,
                message=body,
                timestamp=datetime.utcnow(),
                message_type='text'
            )
            db.session.add(archived)
            db.session.commit()
        except Exception as e:
            logger.warning(f"Could not archive incoming message: {e}")
            db.session.rollback()


# Module-level singleton
_chatbot_service: Optional[ChatbotService] = None


def get_chatbot_service() -> ChatbotService:
    """Return a shared ChatbotService instance."""
    global _chatbot_service
    if _chatbot_service is None:
        _chatbot_service = ChatbotService()
    return _chatbot_service
