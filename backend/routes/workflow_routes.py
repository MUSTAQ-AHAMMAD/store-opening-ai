"""
Workflow Routes for Store Opening Process
API endpoints for managing the 7-stage workflow
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.database import db
from backend.models.models import (
    Store, WorkflowStage, NearbyStoreDetails, MaterialTracking,
    TeamViewerSession, TeamMember, EscalationHistory
)
from backend.services.workflow_service import get_workflow_service
from backend.services.email_service import get_email_service

bp = Blueprint('workflow', __name__, url_prefix='/api/workflow')


@bp.route('/store/<int:store_id>/stages', methods=['GET'])
def get_workflow_stages(store_id):
    """Get all workflow stages for a store"""
    store = Store.query.get_or_404(store_id)
    stages = WorkflowStage.query.filter_by(store_id=store_id).order_by(WorkflowStage.stage_number).all()
    
    return jsonify({
        'store': store.to_dict(),
        'stages': [stage.to_dict() for stage in stages]
    }), 200


@bp.route('/store/<int:store_id>/stages/<int:stage_number>', methods=['GET'])
def get_workflow_stage(store_id, stage_number):
    """Get a specific workflow stage"""
    stage = WorkflowStage.query.filter_by(
        store_id=store_id,
        stage_number=stage_number
    ).first_or_404()
    
    return jsonify(stage.to_dict()), 200


@bp.route('/store/<int:store_id>/nearby-store', methods=['POST'])
def update_nearby_store_details(store_id):
    """Stage 1: Update nearby store details"""
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['store_name', 'contact_person_name', 'contact_person_mobile', 'updated_by_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    updated_by = TeamMember.query.get(data['updated_by_id'])
    if not updated_by:
        return jsonify({'error': 'Team member not found'}), 404
    
    workflow_service = get_workflow_service()
    success = workflow_service.update_nearby_store_details(store, data, updated_by)
    
    if success:
        nearby_store = NearbyStoreDetails.query.filter_by(store_id=store_id).first()
        return jsonify({
            'message': 'Nearby store details updated successfully',
            'nearby_store': nearby_store.to_dict() if nearby_store else None
        }), 200
    else:
        return jsonify({'error': 'Failed to update nearby store details'}), 500


@bp.route('/store/<int:store_id>/nearby-store', methods=['GET'])
def get_nearby_store_details(store_id):
    """Get nearby store details"""
    nearby_store = NearbyStoreDetails.query.filter_by(store_id=store_id).first()
    
    if not nearby_store:
        return jsonify({'message': 'Nearby store details not yet provided'}), 404
    
    return jsonify(nearby_store.to_dict()), 200


@bp.route('/store/<int:store_id>/warehouse-shipment', methods=['POST'])
def confirm_warehouse_shipment(store_id):
    """Stage 2: Confirm checklist complete and sent to warehouse"""
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    
    if 'confirmed_by_id' not in data:
        return jsonify({'error': 'Missing required field: confirmed_by_id'}), 400
    
    confirmed_by = TeamMember.query.get(data['confirmed_by_id'])
    if not confirmed_by:
        return jsonify({'error': 'Team member not found'}), 404
    
    workflow_service = get_workflow_service()
    success = workflow_service.confirm_warehouse_shipment(store, confirmed_by)
    
    if success:
        return jsonify({'message': 'Warehouse shipment confirmed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to confirm warehouse shipment'}), 500


@bp.route('/store/<int:store_id>/nearby-store-receipt', methods=['POST'])
def confirm_nearby_store_receipt(store_id):
    """Stage 3: Confirm material reached nearby store"""
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    
    if 'confirmed_by_id' not in data:
        return jsonify({'error': 'Missing required field: confirmed_by_id'}), 400
    
    confirmed_by = TeamMember.query.get(data['confirmed_by_id'])
    if not confirmed_by:
        return jsonify({'error': 'Team member not found'}), 404
    
    workflow_service = get_workflow_service()
    success = workflow_service.confirm_nearby_store_receipt(store, confirmed_by)
    
    if success:
        return jsonify({'message': 'Nearby store receipt confirmed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to confirm nearby store receipt'}), 500


@bp.route('/store/<int:store_id>/store-receipt', methods=['POST'])
def confirm_store_receipt(store_id):
    """Stage 4: Confirm material reached actual store"""
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    
    if 'confirmed_by_id' not in data:
        return jsonify({'error': 'Missing required field: confirmed_by_id'}), 400
    
    confirmed_by = TeamMember.query.get(data['confirmed_by_id'])
    if not confirmed_by:
        return jsonify({'error': 'Team member not found'}), 404
    
    workflow_service = get_workflow_service()
    success = workflow_service.confirm_store_receipt(store, confirmed_by)
    
    if success:
        return jsonify({'message': 'Store receipt confirmed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to confirm store receipt'}), 500


@bp.route('/store/<int:store_id>/installation', methods=['POST'])
def start_installation(store_id):
    """Stage 5: Start installation and update TeamViewer ID"""
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    
    required_fields = ['teamviewer_id', 'technician_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    technician = TeamMember.query.get(data['technician_id'])
    if not technician:
        return jsonify({'error': 'Technician not found'}), 404
    
    workflow_service = get_workflow_service()
    success = workflow_service.start_installation(store, data['teamviewer_id'], technician)
    
    if success:
        teamviewer_session = TeamViewerSession.query.filter_by(store_id=store_id).first()
        return jsonify({
            'message': 'Installation started successfully',
            'teamviewer_session': teamviewer_session.to_dict() if teamviewer_session else None
        }), 200
    else:
        return jsonify({'error': 'Failed to start installation'}), 500


@bp.route('/store/<int:store_id>/installation', methods=['GET'])
def get_installation_details(store_id):
    """Get TeamViewer installation details"""
    teamviewer_session = TeamViewerSession.query.filter_by(store_id=store_id).first()
    
    if not teamviewer_session:
        return jsonify({'message': 'Installation not yet started'}), 404
    
    return jsonify(teamviewer_session.to_dict()), 200


@bp.route('/store/<int:store_id>/installation', methods=['PUT'])
def update_installation_notes(store_id):
    """Update installation support notes"""
    teamviewer_session = TeamViewerSession.query.filter_by(store_id=store_id).first_or_404()
    data = request.get_json()
    
    if 'support_notes' in data:
        teamviewer_session.support_notes = data['support_notes']
    
    if 'is_active' in data:
        teamviewer_session.is_active = data['is_active']
    
    teamviewer_session.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Installation notes updated successfully',
        'teamviewer_session': teamviewer_session.to_dict()
    }), 200


@bp.route('/store/<int:store_id>/final-checklist', methods=['POST'])
def complete_final_checklist(store_id):
    """Stage 6: Complete final checklist on opening day"""
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    
    if 'completed_by_id' not in data:
        return jsonify({'error': 'Missing required field: completed_by_id'}), 400
    
    completed_by = TeamMember.query.get(data['completed_by_id'])
    if not completed_by:
        return jsonify({'error': 'Team member not found'}), 404
    
    workflow_service = get_workflow_service()
    success = workflow_service.complete_final_checklist(store, completed_by)
    
    if success:
        return jsonify({'message': 'Final checklist completed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to complete final checklist'}), 500


@bp.route('/store/<int:store_id>/complete', methods=['POST'])
def complete_store_opening(store_id):
    """Stage 7: Mark store opening as complete"""
    store = Store.query.get_or_404(store_id)
    
    workflow_service = get_workflow_service()
    success = workflow_service.complete_store_opening(store)
    
    if success:
        return jsonify({'message': 'Store opening completed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to complete store opening'}), 500


@bp.route('/store/<int:store_id>/material-tracking', methods=['GET'])
def get_material_tracking(store_id):
    """Get material tracking information"""
    material_tracking = MaterialTracking.query.filter_by(store_id=store_id).first()
    
    if not material_tracking:
        return jsonify({'message': 'Material tracking not yet available'}), 404
    
    return jsonify(material_tracking.to_dict()), 200


@bp.route('/store/<int:store_id>/opening-date', methods=['PUT'])
def update_opening_date(store_id):
    """Update store opening date and recalculate timelines"""
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    
    if 'opening_date' not in data:
        return jsonify({'error': 'Missing required field: opening_date'}), 400
    
    try:
        new_opening_date = datetime.fromisoformat(data['opening_date'].replace('Z', '+00:00'))
        old_opening_date = store.opening_date
        
        workflow_service = get_workflow_service()
        success = workflow_service.recalculate_timelines(store, new_opening_date)
        
        if success:
            # Send email notification
            email_service = get_email_service()
            team_emails = [m.email for m in store.team_members if m.email and m.is_active]
            
            if team_emails:
                email_service.send_opening_date_change_email(
                    store.to_dict(),
                    old_opening_date.strftime('%Y-%m-%d'),
                    new_opening_date.strftime('%Y-%m-%d'),
                    team_emails
                )
            
            return jsonify({
                'message': 'Opening date updated and timelines recalculated successfully',
                'store': store.to_dict(),
                'stages': [stage.to_dict() for stage in store.workflow_stages]
            }), 200
        else:
            return jsonify({'error': 'Failed to update opening date'}), 500
            
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400


@bp.route('/store/<int:store_id>/escalations', methods=['GET'])
def get_escalations(store_id):
    """Get escalation history for a store"""
    store = Store.query.get_or_404(store_id)
    
    escalations = []
    for stage in store.workflow_stages:
        for escalation in stage.escalations:
            escalations.append(escalation.to_dict())
    
    return jsonify({
        'store_id': store_id,
        'escalations': escalations
    }), 200


@bp.route('/store/<int:store_id>/delayed-stages', methods=['GET'])
def get_delayed_stages(store_id):
    """Get delayed workflow stages for a store"""
    store = Store.query.get_or_404(store_id)
    
    workflow_service = get_workflow_service()
    delayed_stages = workflow_service.check_stage_delays(store)
    
    return jsonify({
        'store_id': store_id,
        'delayed_stages': [stage.to_dict() for stage in delayed_stages]
    }), 200
