"""
Tests for authentication - verifies demo credentials and admin login work correctly.
"""

import json
import pytest
from app import app, db
from backend.models.models import User


@pytest.fixture
def client():
    """Create test client with fresh database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Seed demo users
        admin = User(
            username='admin',
            email='admin@storeai.com',
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')

        manager = User(
            username='manager',
            email='manager@storeai.com',
            full_name='Store Manager',
            role='manager',
            is_active=True
        )
        manager.set_password('manager123')

        team_member = User(
            username='user',
            email='user@storeai.com',
            full_name='Team Member',
            role='team_member',
            is_active=True
        )
        team_member.set_password('user123')

        db.session.add_all([admin, manager, team_member])
        db.session.commit()

        with app.test_client() as client:
            yield client

        db.drop_all()


def test_admin_login(client):
    """Test admin can login with demo credentials"""
    resp = client.post('/api/auth/login',
        data=json.dumps({'username': 'admin', 'password': 'admin123'}),
        content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['message'] == 'Login successful'
    assert data['user']['role'] == 'admin'
    assert 'token' in data


def test_manager_login(client):
    """Test manager can login with demo credentials"""
    resp = client.post('/api/auth/login',
        data=json.dumps({'username': 'manager', 'password': 'manager123'}),
        content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['user']['role'] == 'manager'


def test_team_member_login(client):
    """Test team member can login with demo credentials"""
    resp = client.post('/api/auth/login',
        data=json.dumps({'username': 'user', 'password': 'user123'}),
        content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['user']['role'] == 'team_member'


def test_wrong_password(client):
    """Test login fails with wrong password"""
    resp = client.post('/api/auth/login',
        data=json.dumps({'username': 'admin', 'password': 'wrongpassword'}),
        content_type='application/json')
    assert resp.status_code == 401
    data = resp.get_json()
    assert 'error' in data


def test_token_verify(client):
    """Test JWT token verification works after login"""
    resp = client.post('/api/auth/login',
        data=json.dumps({'username': 'admin', 'password': 'admin123'}),
        content_type='application/json')
    token = resp.get_json()['token']

    resp2 = client.get('/api/auth/verify',
        headers={'Authorization': f'Bearer {token}'})
    assert resp2.status_code == 200
    data = resp2.get_json()
    assert data['user']['username'] == 'admin'


def test_admin_list_users(client):
    """Test admin can list all users"""
    resp = client.post('/api/auth/login',
        data=json.dumps({'username': 'admin', 'password': 'admin123'}),
        content_type='application/json')
    token = resp.get_json()['token']

    resp2 = client.get('/api/auth/users',
        headers={'Authorization': f'Bearer {token}'})
    assert resp2.status_code == 200
    users = resp2.get_json()
    assert len(users) == 3
