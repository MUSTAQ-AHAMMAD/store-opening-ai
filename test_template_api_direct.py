#!/usr/bin/env python3
"""
Test the WhatsApp template API endpoint directly
"""
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set test mode for testing
os.environ['TEST_MODE'] = 'true'

from flask import Flask
from backend.routes.whatsapp_routes import bp as whatsapp_bp
from backend.services.whatsapp_service import WhatsAppService

# Create a simple Flask app for testing
app = Flask(__name__)
app.register_blueprint(whatsapp_bp)

def test_send_template_endpoint():
    """Test the /api/whatsapp/send-template endpoint"""
    print("=" * 70)
    print("🧪 TESTING /api/whatsapp/send-template ENDPOINT")
    print("=" * 70)
    
    with app.test_client() as client:
        # Test 1: Valid template message
        print("\n📱 Test 1: Valid template message")
        print("-" * 70)
        
        response = client.post(
            '/api/whatsapp/send-template',
            json={
                'phone': '+966555313890',
                'content_sid': 'HXb5b62575e6e4ff6129ad7c8efe1f983e',
                'content_variables': {
                    '1': '12/1',
                    '2': '3pm'
                }
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json, indent=2)}")
        
        # Test 2: Missing phone number
        print("\n❌ Test 2: Missing phone number")
        print("-" * 70)
        
        response = client.post(
            '/api/whatsapp/send-template',
            json={
                'content_sid': 'HXb5b62575e6e4ff6129ad7c8efe1f983e'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json, indent=2)}")
        
        # Test 3: Missing content_sid
        print("\n❌ Test 3: Missing content_sid")
        print("-" * 70)
        
        response = client.post(
            '/api/whatsapp/send-template',
            json={
                'phone': '+966555313890'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json, indent=2)}")
        
        # Test 4: Template with no variables
        print("\n📱 Test 4: Template with no variables")
        print("-" * 70)
        
        response = client.post(
            '/api/whatsapp/send-template',
            json={
                'phone': '+966555313890',
                'content_sid': 'HXb5b62575e6e4ff6129ad7c8efe1f983e'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json, indent=2)}")

def test_send_follow_up_endpoint():
    """Test backward compatibility with /api/whatsapp/send-follow-up"""
    print("\n" + "=" * 70)
    print("🧪 TESTING BACKWARD COMPATIBILITY - /api/whatsapp/send-follow-up")
    print("=" * 70)
    
    with app.test_client() as client:
        # Test regular message
        print("\n📝 Test: Regular text message")
        print("-" * 70)
        
        response = client.post(
            '/api/whatsapp/send-follow-up',
            json={
                'phone': '+966555313890',
                'message': 'This is a regular text message for testing'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json, indent=2)}")

if __name__ == "__main__":
    print("\n")
    test_send_template_endpoint()
    test_send_follow_up_endpoint()
    print("\n" + "=" * 70)
    print("✅ ALL API ENDPOINT TESTS COMPLETE")
    print("=" * 70)
    print()
