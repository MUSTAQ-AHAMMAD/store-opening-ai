# WhatsApp Template Messages Guide

## Overview

WhatsApp template messages allow you to send pre-approved message templates with dynamic variables. This is essential for business communication on WhatsApp, as it ensures compliance with WhatsApp's messaging policies.

## What are Template Messages?

Template messages (also called Content Templates) are pre-approved message formats that you create in your Twilio account. They contain placeholders for dynamic content that can be filled in when sending the message.

### Benefits:
- ✅ **Compliant**: Meets WhatsApp's business messaging requirements
- ✅ **Consistent**: Ensures uniform messaging across your organization
- ✅ **Flexible**: Supports dynamic variables for personalization
- ✅ **Professional**: Pre-approved templates maintain quality standards

## API Endpoint

### Send Template Message

**Endpoint:** `POST /api/whatsapp/send-template`

**Request Body:**
```json
{
  "phone": "+966555313890",
  "content_sid": "HXb5b62575e6e4ff6129ad7c8efe1f983e",
  "content_variables": {
    "1": "12/1",
    "2": "3pm"
  }
}
```

**Parameters:**
- `phone` (required): Recipient's phone number in E.164 format (e.g., +966555313890)
- `content_sid` (required): The Content SID from your Twilio Content Template
- `content_variables` (optional): Object containing variables to fill template placeholders

**Response (Success):**
```json
{
  "message": "Template message sent successfully",
  "result": {
    "success": true,
    "message_sid": "SM1234567890abcdef",
    "status": "queued"
  }
}
```

**Response (Error):**
```json
{
  "error": "Phone number is required"
}
```

## Using the API

### Example 1: Using curl

```bash
curl -X POST 'http://localhost:5000/api/whatsapp/send-template' \
  -H 'Content-Type: application/json' \
  -d '{
    "phone": "+966555313890",
    "content_sid": "HXb5b62575e6e4ff6129ad7c8efe1f983e",
    "content_variables": {
      "1": "12/1",
      "2": "3pm"
    }
  }'
```

### Example 2: Using Python

```python
import requests
import json

url = "http://localhost:5000/api/whatsapp/send-template"

payload = {
    "phone": "+966555313890",
    "content_sid": "HXb5b62575e6e4ff6129ad7c8efe1f983e",
    "content_variables": {
        "1": "12/1",
        "2": "3pm"
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

### Example 3: Using JavaScript/Node.js

```javascript
const axios = require('axios');

const data = {
  phone: '+966555313890',
  content_sid: 'HXb5b62575e6e4ff6129ad7c8efe1f983e',
  content_variables: {
    '1': '12/1',
    '2': '3pm'
  }
};

axios.post('http://localhost:5000/api/whatsapp/send-template', data)
  .then(response => {
    console.log('Success:', response.data);
  })
  .catch(error => {
    console.error('Error:', error.response.data);
  });
```

## Creating Content Templates in Twilio

Before you can send template messages, you need to create them in your Twilio account:

1. **Log in to Twilio Console**
   - Go to https://console.twilio.com

2. **Navigate to Content Templates**
   - Messaging → Content Editor → Templates

3. **Create a New Template**
   - Click "Create new Template"
   - Choose your message type (WhatsApp)
   - Define your template with placeholders using {{1}}, {{2}}, etc.

4. **Get the Content SID**
   - After creating, copy the Content SID (starts with HX...)
   - Use this SID in your API calls

### Example Template:

```
Your appointment is scheduled for {{1}} at {{2}}. 
Please arrive 10 minutes early. Reply CONFIRM to confirm.
```

Variables:
- `{{1}}` = Date (e.g., "12/1")
- `{{2}}` = Time (e.g., "3pm")

## Direct Twilio API Usage

If you prefer to use Twilio's API directly (without our application layer):

```bash
curl 'https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json' \
  -X POST \
  --data-urlencode 'To=whatsapp:+966555313890' \
  --data-urlencode 'From=whatsapp:+14155238886' \
  --data-urlencode 'ContentSid=HXb5b62575e6e4ff6129ad7c8efe1f983e' \
  --data-urlencode 'ContentVariables={"1":"12/1","2":"3pm"}' \
  -u {AccountSid}:{AuthToken}
```

Replace `{AccountSid}` and `{AuthToken}` with your actual Twilio credentials.

## Service Layer Usage

You can also use the WhatsApp service directly in your Python code:

```python
from backend.services.whatsapp_service import WhatsAppService

service = WhatsAppService()

# Send template message
result = service.send_message(
    to_phone="+966555313890",
    content_sid="HXb5b62575e6e4ff6129ad7c8efe1f983e",
    content_variables={
        "1": "12/1",
        "2": "3pm"
    }
)

print(result)
# Output: {'success': True, 'message_sid': 'SM...', 'status': 'queued'}
```

## Backward Compatibility

The existing `send_message` method still works for regular text messages:

```python
# Regular text message (still works)
result = service.send_message(
    to_phone="+966555313890",
    message="This is a regular text message"
)
```

Both template messages and regular messages are supported in the same method, making it flexible for different use cases.

## Test Mode

When `TEST_MODE=true` in your `.env` file, template messages will be logged to the console instead of being sent:

```
============================================================
📱 WhatsApp Message (Test Mode)
============================================================
To: whatsapp:+966555313890
Time: 2026-02-18 01:46:13
Template Message:
  Content SID: HXb5b62575e6e4ff6129ad7c8efe1f983e
  Variables: {'1': '12/1', '2': '3pm'}
============================================================
```

This is useful for:
- Development and testing
- Debugging message templates
- Avoiding costs during development
- Testing without a Twilio account

## Common Use Cases

### 1. Appointment Reminders

```json
{
  "phone": "+1234567890",
  "content_sid": "HX_appointment_reminder",
  "content_variables": {
    "1": "Dr. Smith",
    "2": "March 15, 2024",
    "3": "2:00 PM"
  }
}
```

### 2. Order Status Updates

```json
{
  "phone": "+1234567890",
  "content_sid": "HX_order_status",
  "content_variables": {
    "1": "Order #12345",
    "2": "Shipped",
    "3": "https://tracking.example.com/12345"
  }
}
```

### 3. Store Opening Notifications

```json
{
  "phone": "+1234567890",
  "content_sid": "HX_store_opening",
  "content_variables": {
    "1": "Downtown Store",
    "2": "December 1, 2024",
    "3": "9:00 AM"
  }
}
```

## Error Handling

### Common Errors:

1. **Missing Content SID**
   ```json
   {"error": "Content SID is required"}
   ```

2. **Missing Phone Number**
   ```json
   {"error": "Phone number is required"}
   ```

3. **Invalid Content SID**
   ```json
   {
     "result": {
       "success": false,
       "error": "Unable to create record: The requested resource /Content/HXinvalid was not found"
     }
   }
   ```

4. **Invalid Template Variables**
   - Ensure all required variables are provided
   - Variable keys must match template placeholders

## Testing

### Run the Test Script

```bash
# Test the service layer
python test_template_message.py

# Test the API endpoints (requires app to be running)
./test_template_api.sh
```

### Manual Testing

1. Start the application:
   ```bash
   python app.py
   ```

2. Send a test template message:
   ```bash
   curl -X POST http://localhost:5000/api/whatsapp/send-template \
     -H 'Content-Type: application/json' \
     -d '{
       "phone": "+1234567890",
       "content_sid": "HXyour_content_sid",
       "content_variables": {"1": "value1", "2": "value2"}
     }'
   ```

## Best Practices

1. **Always use E.164 format** for phone numbers (+country_code + number)
2. **Create templates in Twilio Console** before using them
3. **Test in TEST_MODE** before going to production
4. **Keep Content SIDs organized** (use descriptive names)
5. **Document your template variables** for team members
6. **Handle errors gracefully** in your application
7. **Monitor message delivery** in Twilio Console

## Resources

- **Twilio Content API**: https://www.twilio.com/docs/content
- **WhatsApp Templates**: https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates
- **Twilio Console**: https://console.twilio.com
- **Message Logs**: https://console.twilio.com/us1/monitor/logs/sms

## Troubleshooting

### Messages not sending?

1. Verify Content SID is correct
2. Check that template is approved in Twilio Console
3. Ensure recipient has joined your WhatsApp sandbox
4. Verify phone number format (E.164)
5. Check Twilio Console logs for detailed errors

### Template variables not working?

1. Ensure variable keys match template placeholders
2. Use string keys (e.g., "1", "2", not 1, 2)
3. Verify JSON format is correct
4. Check template definition in Twilio Console

---

**Need Help?** Check the Twilio documentation or contact support at support@twilio.com
