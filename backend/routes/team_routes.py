from flask import Blueprint, request, jsonify
from app import db
from backend.models.models import TeamMember, Store

bp = Blueprint('team', __name__, url_prefix='/api/team')

@bp.route('', methods=['GET'])
def get_team_members():
    """Get all team members"""
    store_id = request.args.get('store_id', type=int)
    
    if store_id:
        team_members = TeamMember.query.filter_by(store_id=store_id).all()
    else:
        team_members = TeamMember.query.all()
    
    return jsonify([member.to_dict() for member in team_members]), 200

@bp.route('/<int:member_id>', methods=['GET'])
def get_team_member(member_id):
    """Get a specific team member"""
    member = TeamMember.query.get_or_404(member_id)
    result = member.to_dict()
    
    # Include task stats
    result['total_tasks'] = len(member.tasks)
    result['completed_tasks'] = len([task for task in member.tasks if task.status == 'completed'])
    result['pending_tasks'] = len([task for task in member.tasks if task.status != 'completed'])
    
    return jsonify(result), 200

@bp.route('', methods=['POST'])
def create_team_member():
    """Create a new team member"""
    data = request.get_json()
    
    try:
        # Verify store exists
        store = Store.query.get_or_404(data['store_id'])
        
        member = TeamMember(
            name=data['name'],
            role=data['role'],
            phone=data['phone'],
            email=data.get('email'),
            store_id=data['store_id'],
            is_active=data.get('is_active', True)
        )
        db.session.add(member)
        db.session.commit()
        
        return jsonify(member.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:member_id>', methods=['PUT'])
def update_team_member(member_id):
    """Update a team member"""
    member = TeamMember.query.get_or_404(member_id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            member.name = data['name']
        if 'role' in data:
            member.role = data['role']
        if 'phone' in data:
            member.phone = data['phone']
        if 'email' in data:
            member.email = data['email']
        if 'is_active' in data:
            member.is_active = data['is_active']
        
        db.session.commit()
        return jsonify(member.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:member_id>', methods=['DELETE'])
def delete_team_member(member_id):
    """Delete a team member"""
    member = TeamMember.query.get_or_404(member_id)
    
    try:
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Team member deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
