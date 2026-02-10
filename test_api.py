#!/usr/bin/env python3
"""
Comprehensive Test Script for Store Opening AI Application
Tests API endpoints, database, and basic functionality
"""

import requests
import sys
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        print("✅ Health endpoint OK")
        return True
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False

def test_stores():
    """Test stores endpoints"""
    print("\nTesting stores endpoints...")
    try:
        # Get all stores
        response = requests.get(f"{API_BASE_URL}/api/stores")
        assert response.status_code == 200
        stores = response.json()
        assert len(stores) > 0
        print(f"✅ GET /api/stores - Found {len(stores)} stores")
        
        # Get specific store
        store_id = stores[0]['id']
        response = requests.get(f"{API_BASE_URL}/api/stores/{store_id}")
        assert response.status_code == 200
        store = response.json()
        assert 'name' in store
        assert 'location' in store
        assert 'total_tasks' in store
        print(f"✅ GET /api/stores/{store_id} - {store['name']}")
        
        return True
    except Exception as e:
        print(f"❌ Stores endpoints failed: {e}")
        return False

def test_team():
    """Test team endpoints"""
    print("\nTesting team endpoints...")
    try:
        # Get all team members
        response = requests.get(f"{API_BASE_URL}/api/team")
        assert response.status_code == 200
        team = response.json()
        assert len(team) > 0
        print(f"✅ GET /api/team - Found {len(team)} team members")
        
        # Get specific team member
        member_id = team[0]['id']
        response = requests.get(f"{API_BASE_URL}/api/team/{member_id}")
        assert response.status_code == 200
        member = response.json()
        assert 'name' in member
        assert 'role' in member
        print(f"✅ GET /api/team/{member_id} - {member['name']}")
        
        return True
    except Exception as e:
        print(f"❌ Team endpoints failed: {e}")
        return False

def test_checklists():
    """Test checklist endpoints"""
    print("\nTesting checklist endpoints...")
    try:
        # Get all checklists
        response = requests.get(f"{API_BASE_URL}/api/checklists")
        assert response.status_code == 200
        checklists = response.json()
        assert len(checklists) > 0
        print(f"✅ GET /api/checklists - Found {len(checklists)} checklists")
        
        # Get tasks for a checklist
        checklist_id = checklists[0]['id']
        response = requests.get(f"{API_BASE_URL}/api/checklists/{checklist_id}/tasks")
        assert response.status_code == 200
        tasks = response.json()
        print(f"✅ GET /api/checklists/{checklist_id}/tasks - Found {len(tasks)} tasks")
        
        return True
    except Exception as e:
        print(f"❌ Checklist endpoints failed: {e}")
        return False

def test_analytics():
    """Test analytics endpoints"""
    print("\nTesting analytics endpoints...")
    try:
        # Get dashboard analytics
        response = requests.get(f"{API_BASE_URL}/api/analytics/dashboard")
        assert response.status_code == 200
        analytics = response.json()
        assert 'summary' in analytics
        summary = analytics['summary']
        assert 'total_stores' in summary
        assert 'total_tasks' in summary
        print(f"✅ GET /api/analytics/dashboard")
        print(f"   Total Stores: {summary['total_stores']}")
        print(f"   Total Tasks: {summary['total_tasks']}")
        print(f"   Completed Tasks: {summary['completed_tasks']}")
        print(f"   Pending Tasks: {summary['pending_tasks']}")
        
        return True
    except Exception as e:
        print(f"❌ Analytics endpoints failed: {e}")
        return False

def test_whatsapp():
    """Test WhatsApp endpoints"""
    print("\nTesting WhatsApp endpoints...")
    try:
        # Get all WhatsApp groups
        response = requests.get(f"{API_BASE_URL}/api/whatsapp/groups")
        assert response.status_code == 200
        groups = response.json()
        print(f"✅ GET /api/whatsapp/groups - Found {len(groups)} groups")
        
        return True
    except Exception as e:
        print(f"❌ WhatsApp endpoints failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Store Opening AI - Comprehensive Test Suite")
    print("="*60)
    
    tests = [
        test_health,
        test_stores,
        test_team,
        test_checklists,
        test_analytics,
        test_whatsapp
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
