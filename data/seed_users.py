"""
Seed Default Admin User
Creates a default admin user for initial login
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from backend.models.models import User

def seed_admin_user(skip_context=False):
    """Create default admin user"""
    def _seed():
        # Ensure database tables exist
        db.create_all()
        
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='admin').first()
        
        if existing_admin:
            print("Users already exist, skipping user creation")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@storeai.com',
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')  # Change this in production!
        
        db.session.add(admin)
        
        # Create demo users
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
        
        db.session.add(manager)
        db.session.add(team_member)
        
        db.session.commit()
        
        print("✓ Default users created successfully!")
        print("\n" + "="*50)
        print("DEFAULT LOGIN CREDENTIALS")
        print("="*50)
        print("\nAdmin Account:")
        print(f"  Username: admin")
        print(f"  Password: admin123")
        print(f"  Email: admin@storeai.com")
        print("\nManager Account:")
        print(f"  Username: manager")
        print(f"  Password: manager123")
        print(f"  Email: manager@storeai.com")
        print("\nTeam Member Account:")
        print(f"  Username: user")
        print(f"  Password: user123")
        print(f"  Email: user@storeai.com")
        print("\n" + "="*50)
        print("⚠️  SECURITY WARNING!")
        print("="*50)
        print("These are DEFAULT passwords for DEVELOPMENT ONLY!")
        print("For PRODUCTION:")
        print("1. Generate strong random passwords")
        print("2. Force password change on first login")
        print("3. Never use predictable passwords like these")
        print("="*50 + "\n")
    
    if skip_context:
        _seed()
    else:
        with app.app_context():
            _seed()

if __name__ == '__main__':
    seed_admin_user()
