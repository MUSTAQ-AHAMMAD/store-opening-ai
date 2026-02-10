"""
Test Store Opening Workflow Automation
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from backend.models.models import (
    Store, WorkflowStage, NearbyStoreDetails, MaterialTracking,
    TeamViewerSession, TeamMember
)
from backend.services.workflow_service import get_workflow_service

# Test constants
DATETIME_TOLERANCE_SECONDS = 60  # Allow 1 minute tolerance for datetime comparisons


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture
def sample_store(client):
    """Create a sample store for testing"""
    with app.app_context():
        opening_date = datetime.utcnow() + timedelta(days=30)
        store = Store(
            name='Test Store',
            location='Test Location',
            opening_date=opening_date,
            status='planning',
            workflow_stage=0
        )
        db.session.add(store)
        db.session.commit()
        
        # Create a test team member
        team_member = TeamMember(
            name='Test Member',
            role='technician',
            phone='+1234567890',
            email='test@example.com',
            store_id=store.id
        )
        db.session.add(team_member)
        db.session.commit()
        
        return store.id, team_member.id


def test_workflow_initialization(client, sample_store):
    """Test workflow stages are initialized correctly"""
    store_id, _ = sample_store
    
    with app.app_context():
        store = Store.query.get(store_id)
        workflow_service = get_workflow_service()
        
        # Initialize workflow
        stages = workflow_service.initialize_workflow(store)
        
        # Check that 7 stages were created
        assert len(stages) == 7
        
        # Check stage 1 is in progress
        assert stages[0].status == 'in_progress'
        assert stages[0].stage_number == 1
        
        # Check other stages are pending
        for i in range(1, 7):
            assert stages[i].status == 'pending'
            assert stages[i].stage_number == i + 1
        
        # Check due dates are set correctly
        for stage in stages:
            assert stage.due_date is not None
            assert stage.due_date <= store.opening_date


def test_nearby_store_update(client, sample_store):
    """Test Stage 1: Update nearby store details"""
    store_id, team_member_id = sample_store
    
    with app.app_context():
        store = Store.query.get(store_id)
        team_member = TeamMember.query.get(team_member_id)
        workflow_service = get_workflow_service()
        
        # Initialize workflow
        workflow_service.initialize_workflow(store)
        
        # Update nearby store details
        details = {
            'store_name': 'Nearby Store ABC',
            'store_address': '123 Test St',
            'contact_person_name': 'John Doe',
            'contact_person_mobile': '+1987654321',
            'distance_km': 5.5
        }
        
        success = workflow_service.update_nearby_store_details(store, details, team_member)
        assert success
        
        # Check nearby store details were saved
        nearby_store = NearbyStoreDetails.query.filter_by(store_id=store_id).first()
        assert nearby_store is not None
        assert nearby_store.store_name == 'Nearby Store ABC'
        assert nearby_store.contact_person_name == 'John Doe'
        
        # Check stage 1 is completed and stage 2 is in progress
        stage1 = WorkflowStage.query.filter_by(store_id=store_id, stage_number=1).first()
        stage2 = WorkflowStage.query.filter_by(store_id=store_id, stage_number=2).first()
        
        assert stage1.status == 'completed'
        assert stage2.status == 'in_progress'


def test_warehouse_shipment(client, sample_store):
    """Test Stage 2: Confirm warehouse shipment"""
    store_id, team_member_id = sample_store
    
    with app.app_context():
        store = Store.query.get(store_id)
        team_member = TeamMember.query.get(team_member_id)
        workflow_service = get_workflow_service()
        
        # Initialize workflow and complete stage 1
        workflow_service.initialize_workflow(store)
        details = {
            'store_name': 'Nearby Store',
            'contact_person_name': 'John',
            'contact_person_mobile': '+1234567890'
        }
        workflow_service.update_nearby_store_details(store, details, team_member)
        
        # Confirm warehouse shipment
        success = workflow_service.confirm_warehouse_shipment(store, team_member)
        assert success
        
        # Check material tracking was created
        material_tracking = MaterialTracking.query.filter_by(store_id=store_id).first()
        assert material_tracking is not None
        assert material_tracking.current_location == 'in_transit'
        assert material_tracking.warehouse_sent_at is not None


def test_installation_start(client, sample_store):
    """Test Stage 5: Start installation with TeamViewer ID"""
    store_id, team_member_id = sample_store
    
    with app.app_context():
        store = Store.query.get(store_id)
        team_member = TeamMember.query.get(team_member_id)
        workflow_service = get_workflow_service()
        
        # Initialize workflow
        workflow_service.initialize_workflow(store)
        
        # Advance to stage 5 (simulating completed stages 1-4)
        for stage_num in range(1, 5):
            stage = WorkflowStage.query.filter_by(store_id=store_id, stage_number=stage_num).first()
            stage.status = 'completed'
            stage.completed_at = datetime.utcnow()
        
        stage5 = WorkflowStage.query.filter_by(store_id=store_id, stage_number=5).first()
        stage5.status = 'in_progress'
        stage5.started_at = datetime.utcnow()
        db.session.commit()
        
        # Start installation
        teamviewer_id = 'TV-123-456-789'
        success = workflow_service.start_installation(store, teamviewer_id, team_member)
        assert success
        
        # Check TeamViewer session was created
        tv_session = TeamViewerSession.query.filter_by(store_id=store_id).first()
        assert tv_session is not None
        assert tv_session.teamviewer_id == teamviewer_id
        assert tv_session.is_active is True


def test_timeline_recalculation(client, sample_store):
    """Test timeline recalculation when opening date changes"""
    store_id, _ = sample_store
    
    with app.app_context():
        store = Store.query.get(store_id)
        workflow_service = get_workflow_service()
        
        # Initialize workflow
        original_opening_date = store.opening_date
        workflow_service.initialize_workflow(store)
        
        # Get original due dates
        original_due_dates = {}
        for stage in store.workflow_stages:
            original_due_dates[stage.stage_number] = stage.due_date
        
        # Change opening date (add 10 days)
        new_opening_date = original_opening_date + timedelta(days=10)
        success = workflow_service.recalculate_timelines(store, new_opening_date)
        assert success
        
        # Check all due dates were updated
        for stage in store.workflow_stages:
            if stage.status != 'completed':
                new_due_date = stage.due_date
                old_due_date = original_due_dates[stage.stage_number]
                
                # New due date should be 10 days later
                expected_due_date = old_due_date + timedelta(days=10)
                assert abs((new_due_date - expected_due_date).total_seconds()) < DATETIME_TOLERANCE_SECONDS


def test_delayed_stage_detection(client, sample_store):
    """Test detection of delayed workflow stages"""
    store_id, _ = sample_store
    
    with app.app_context():
        store = Store.query.get(store_id)
        workflow_service = get_workflow_service()
        
        # Initialize workflow
        workflow_service.initialize_workflow(store)
        
        # Set stage 1 due date to past
        stage1 = WorkflowStage.query.filter_by(store_id=store_id, stage_number=1).first()
        stage1.due_date = datetime.utcnow() - timedelta(days=3)
        db.session.commit()
        
        # Check for delayed stages
        delayed_stages = workflow_service.check_stage_delays(store)
        
        assert len(delayed_stages) > 0
        assert delayed_stages[0].stage_number == 1
        assert delayed_stages[0].status == 'in_progress'


def test_complete_workflow(client, sample_store):
    """Test completing the entire workflow"""
    store_id, team_member_id = sample_store
    
    with app.app_context():
        store = Store.query.get(store_id)
        team_member = TeamMember.query.get(team_member_id)
        workflow_service = get_workflow_service()
        
        # Initialize workflow
        workflow_service.initialize_workflow(store)
        
        # Stage 1: Update nearby store
        workflow_service.update_nearby_store_details(store, {
            'store_name': 'Nearby',
            'contact_person_name': 'John',
            'contact_person_mobile': '+1234567890'
        }, team_member)
        
        # Stage 2: Warehouse shipment
        workflow_service.confirm_warehouse_shipment(store, team_member)
        
        # Stage 3: Nearby store receipt
        workflow_service.confirm_nearby_store_receipt(store, team_member)
        
        # Stage 4: Store receipt
        workflow_service.confirm_store_receipt(store, team_member)
        
        # Stage 5: Installation
        workflow_service.start_installation(store, 'TV-123', team_member)
        
        # Stage 6: Final checklist
        workflow_service.complete_final_checklist(store, team_member)
        
        # Stage 7: Complete
        success = workflow_service.complete_store_opening(store)
        assert success
        
        # Check store status
        assert store.status == 'completed'
        assert store.workflow_stage == 7
        
        # Check all stages are completed
        for stage in store.workflow_stages:
            assert stage.status == 'completed'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
