#!/usr/bin/env python3
"""
Test script to verify Twilio WhatsApp configuration
"""
import os
import sys
from dotenv import load_dotenv
from twilio.rest import Client

def test_twilio_config():
    """Test Twilio configuration"""
    print("=" * 70)
    print("🔧 TWILIO WHATSAPP CONFIGURATION TEST")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
    test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
    
    print("\n📋 Configuration Status:")
    print(f"   • Account SID: {'✓ Set' if account_sid else '✗ Missing'}")
    if account_sid:
        print(f"     Value: {account_sid[:10]}...{account_sid[-4:]}")
    
    print(f"   • Auth Token: {'✓ Set' if auth_token else '✗ Missing'}")
    if auth_token:
        print(f"     Value: {'*' * 30}{auth_token[-4:]}")
    
    print(f"   • WhatsApp Number: {whatsapp_number or '✗ Missing'}")
    print(f"   • Test Mode: {'ENABLED' if test_mode else 'DISABLED'}")
    
    # Validate credentials
    if not account_sid or not auth_token:
        print("\n❌ ERROR: Twilio credentials are missing!")
        print("   Please check your .env file.")
        return False
    
    if test_mode:
        print("\n⚠️  WARNING: TEST_MODE is enabled!")
        print("   Messages will be logged only, not sent via Twilio.")
        print("   Set TEST_MODE=false in .env to enable real Twilio integration.")
        return True
    
    # Try to connect to Twilio
    print("\n🔌 Testing Twilio Connection...")
    try:
        client = Client(account_sid, auth_token)
        
        # Fetch account details to verify credentials
        account = client.api.accounts(account_sid).fetch()
        
        print(f"   ✓ Connection successful!")
        print(f"   • Account Name: {account.friendly_name}")
        print(f"   • Account Status: {account.status}")
        print(f"   • Account Type: {account.type}")
        
        # Show WhatsApp sandbox info
        print(f"\n📱 WhatsApp Sandbox Configuration:")
        print(f"   • Sandbox Number: {whatsapp_number}")
        print(f"   • Join Code: valuable-connected")
        print(f"   • Sandbox URL: https://timberwolf-mastiff-9776.twil.io/demo-reply")
        print(f"\n   To test, send a WhatsApp message to {whatsapp_number}")
        print(f"   with the message: join valuable-connected")
        
        print("\n✅ Configuration Test PASSED!")
        print("   Your Twilio WhatsApp integration is ready to use!")
        return True
        
    except Exception as e:
        print(f"   ✗ Connection failed!")
        print(f"   Error: {str(e)}")
        print("\n❌ Configuration Test FAILED!")
        print("   Please verify your Twilio credentials.")
        return False

if __name__ == "__main__":
    print()
    success = test_twilio_config()
    print("\n" + "=" * 70)
    
    sys.exit(0 if success else 1)
