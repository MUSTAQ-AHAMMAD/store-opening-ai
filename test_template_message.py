#!/usr/bin/env python3
"""
Test script for WhatsApp template message functionality
"""
import os
import sys
import json
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.whatsapp_service import WhatsAppService

def test_template_message():
    """Test sending a WhatsApp template message"""
    print("=" * 70)
    print("🧪 WHATSAPP TEMPLATE MESSAGE TEST")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize service
    service = WhatsAppService()
    
    print("\n📋 Service Configuration:")
    print(f"   • Account SID: {'✓ Set' if service.account_sid else '✗ Missing'}")
    print(f"   • Auth Token: {'✓ Set' if service.auth_token else '✗ Missing'}")
    print(f"   • WhatsApp Number: {service.whatsapp_number}")
    print(f"   • Test Mode: {'ENABLED' if service.test_mode else 'DISABLED'}")
    print(f"   • Twilio Client: {'✓ Initialized' if service.client else '✗ Not Initialized'}")
    
    # Test data from the curl command
    test_phone = "+966555313890"
    test_content_sid = "HXb5b62575e6e4ff6129ad7c8efe1f983e"
    test_variables = {
        "1": "12/1",
        "2": "3pm"
    }
    
    print(f"\n📱 Test Template Message:")
    print(f"   • To: {test_phone}")
    print(f"   • Content SID: {test_content_sid}")
    print(f"   • Variables: {json.dumps(test_variables, indent=2)}")
    
    # Send template message
    print(f"\n🚀 Sending template message...")
    result = service.send_message(
        to_phone=test_phone,
        content_sid=test_content_sid,
        content_variables=test_variables
    )
    
    print(f"\n📊 Result:")
    print(f"   • Success: {result.get('success')}")
    if result.get('success'):
        print(f"   • Message SID: {result.get('message_sid', 'N/A')}")
        print(f"   • Status: {result.get('status', 'N/A')}")
        if result.get('simulated'):
            print(f"   • Mode: Test/Simulated")
            print(f"   • Timestamp: {result.get('timestamp', 'N/A')}")
    else:
        print(f"   • Error: {result.get('error')}")
    
    # Test with regular message (backward compatibility)
    print(f"\n" + "=" * 70)
    print("🧪 TESTING BACKWARD COMPATIBILITY (Regular Message)")
    print("=" * 70)
    
    test_message = "This is a regular text message"
    print(f"\n📱 Test Regular Message:")
    print(f"   • To: {test_phone}")
    print(f"   • Message: {test_message}")
    
    print(f"\n🚀 Sending regular message...")
    result2 = service.send_message(
        to_phone=test_phone,
        message=test_message
    )
    
    print(f"\n📊 Result:")
    print(f"   • Success: {result2.get('success')}")
    if result2.get('success'):
        print(f"   • Message SID: {result2.get('message_sid', 'N/A')}")
        print(f"   • Status: {result2.get('status', 'N/A')}")
        if result2.get('simulated'):
            print(f"   • Mode: Test/Simulated")
    else:
        print(f"   • Error: {result2.get('error')}")
    
    # Test error case (no message or content_sid)
    print(f"\n" + "=" * 70)
    print("🧪 TESTING ERROR HANDLING (No Message or ContentSid)")
    print("=" * 70)
    
    print(f"\n🚀 Attempting to send without message or content_sid...")
    result3 = service.send_message(to_phone=test_phone)
    
    print(f"\n📊 Result:")
    print(f"   • Success: {result3.get('success')}")
    print(f"   • Error: {result3.get('error')}")
    
    print("\n" + "=" * 70)
    print("✅ TEMPLATE MESSAGE TEST COMPLETE")
    print("=" * 70)
    print()

if __name__ == "__main__":
    test_template_message()
