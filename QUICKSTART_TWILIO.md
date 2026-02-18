# 🚀 Quick Start - Twilio WhatsApp Testing

## ✅ Configuration Complete!

Your application is **ready to test** with Twilio WhatsApp integration.

## 📱 Step 1: Join the Sandbox (Required!)

Before testing, join the WhatsApp sandbox:

1. **Open WhatsApp** on your device
2. **Send a message to**: `+1 415 523 8886`
3. **Message text**: `join valuable-connected`
4. **Wait for confirmation** message from Twilio

> ⚠️ **Important**: You must do this step first, or messages won't be delivered!

## 🎯 Step 2: Start the Application

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Start the backend
python app.py
```

The server starts at: **http://localhost:5000**

## 🧪 Step 3: Test WhatsApp Integration

### Option A: Via Python Script

```python
from backend.services.whatsapp_service import WhatsAppService

service = WhatsAppService()
result = service.send_message(
    to_phone="+1234567890",  # Replace with your WhatsApp number
    message="Hello from Store Opening AI! 🎉"
)
print(result)
```

### Option B: Via API

```bash
curl -X POST http://localhost:5000/api/whatsapp/send-follow-up \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890",
    "message": "Test message from Store Opening AI"
  }'
```

### Option C: Via Dashboard

1. Go to **http://localhost:5000**
2. Login with: `admin` / `admin123`
3. Navigate to **Stores** → **Create Store**
4. Add **Team Members** with phone numbers
5. Create **Tasks** with notifications
6. Watch WhatsApp messages arrive! 📱

## ⚙️ Configuration Details

Location: `.env` file in project root

```bash
TWILIO_ACCOUNT_SID=AC4539ac9d...994f
TWILIO_AUTH_TOKEN=***************
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TEST_MODE=false  # Set to 'true' to test without sending real messages
```

## 🔧 Troubleshooting

### Messages not received?

✅ **Verify you joined the sandbox** (send `join valuable-connected` to `+1 415 523 8886`)  
✅ **Check phone format** - Use E.164 format (e.g., `+14155238886`)  
✅ **View Twilio Console** - https://console.twilio.com/us1/monitor/logs/sms  
✅ **Check application logs** - Look for "WhatsApp service initialized with Twilio"  

### Want to test without real messages?

Edit `.env` and set:
```bash
TEST_MODE=true
```

This will log messages to console instead of sending them.

## 📚 Documentation

- **Full Setup Guide**: `TWILIO_SETUP_COMPLETE.md`
- **Test Mode Guide**: `TEST_MODE_GUIDE.md`
- **Main README**: `README.md`

## 🎉 What's Working

✅ Twilio credentials configured  
✅ WhatsApp sandbox ready  
✅ Backend service initialized  
✅ API endpoints active  
✅ Test mode available  
✅ Automatic notifications enabled  

## 🎯 Next Steps

1. ✅ Join the sandbox (critical!)
2. ✅ Start the app
3. ✅ Test with your phone number
4. ✅ Add team members and create tasks
5. ✅ Watch the automation work!

---

**Need Help?** Check `TWILIO_SETUP_COMPLETE.md` for detailed instructions.

**Security Note**: The `.env` file is excluded from git to keep your credentials safe.
