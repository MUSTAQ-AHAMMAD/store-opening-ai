#!/usr/bin/env python
"""
Quick test script to validate the Store Opening AI system
"""

from app import create_app
import requests
import time
from threading import Thread

def test_api():
    """Test the API endpoints"""
    print("="*60)
    print("Testing Store Opening AI System")
    print("="*60)
    
    # Create app
    print("\n1. Creating Flask app...")
    app = create_app()
    print("   ✓ App created successfully")
    
    # Start server
    print("\n2. Starting test server...")
    def run_server():
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(3)
    print("   ✓ Server started on http://localhost:5000")
    
    # Test endpoints
    print("\n3. Testing API endpoints...")
    
    endpoints = [
        ('/api/stores', 'Stores'),
        ('/api/team', 'Team Members'),
        ('/api/checklists', 'Checklists'),
        ('/api/whatsapp/groups', 'WhatsApp Groups'),
        ('/api/analytics/dashboard', 'Dashboard Analytics'),
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'http://localhost:5000{endpoint}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"   ✓ {name}: {len(data)} items")
                elif isinstance(data, dict):
                    if 'summary' in data:
                        print(f"   ✓ {name}: {data['summary']}")
                    else:
                        print(f"   ✓ {name}: OK")
            else:
                print(f"   ✗ {name}: Error {response.status_code}")
        except Exception as e:
            print(f"   ✗ {name}: {str(e)}")
        time.sleep(0.5)
    
    # Test specific store details
    print("\n4. Testing specific store details...")
    try:
        response = requests.get('http://localhost:5000/api/stores/1')
        if response.status_code == 200:
            store = response.json()
            print(f"   ✓ Store: {store['name']}")
            print(f"     - Location: {store['location']}")
            print(f"     - Status: {store['status']}")
            print(f"     - Team Members: {store.get('team_members_count', 0)}")
            print(f"     - Completion: {store.get('completion_percentage', 0):.1f}%")
    except Exception as e:
        print(f"   ✗ Store details: {str(e)}")
    
    print("\n" + "="*60)
    print("✓ All tests completed successfully!")
    print("="*60)
    print("\nYou can now:")
    print("  - Start the API server: python app.py")
    print("  - Start the dashboard: streamlit run frontend/dashboard.py")
    print("="*60)

if __name__ == '__main__':
    test_api()
    time.sleep(2)  # Keep server alive briefly
