# Test Mode Guide

## Overview

The Store Opening AI Management System now includes a **Test Mode** feature that allows you to test all functionality without requiring Twilio accounts, phone numbers, or email configurations.

## Features

### What Works in Test Mode

✅ **All System Features** - Every feature of the system works normally
✅ **WhatsApp Messages** - Logged to console with full formatting
✅ **Voice Calls** - Call scripts displayed with all details
✅ **SMS Messages** - Shown with recipient and content
✅ **Email Notifications** - Displays subject, recipients, and body
✅ **Dashboard UI** - Shows a clear test mode indicator
✅ **Workflow Automation** - All 7 stages work normally
✅ **Task Management** - Create, update, and track tasks
✅ **Team Management** - Manage team members across stores
✅ **Analytics** - View all charts and reports

## Setup

### 1. Enable Test Mode

Edit your `.env` file:

```bash
# Test Mode (for testing without Twilio/Email)
TEST_MODE=true
```

### 2. Configure Minimal Settings

You still need these basic settings, but Twilio and Email can use placeholder values:

```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///store_opening.db

# Twilio Configuration (can be placeholders in test mode)
TWILIO_ACCOUNT_SID=placeholder
TWILIO_AUTH_TOKEN=placeholder
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+1234567890

# Email Configuration (can be placeholders in test mode)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=placeholder@gmail.com
SMTP_PASSWORD=placeholder
FROM_EMAIL=placeholder@gmail.com

# Scheduler Configuration
SCHEDULER_TIMEZONE=UTC
ENABLE_SCHEDULER=true

# Test Mode
TEST_MODE=true
```

### 3. Run the Application

```bash
# Terminal 1: Start backend
python app.py

# Terminal 2: Start dashboard
streamlit run frontend/dashboard.py
```

## Test Mode Indicators

### Dashboard Banner

When in test mode, you'll see a prominent yellow banner at the top of the dashboard:

```
🧪 TEST MODE: All messages (WhatsApp, SMS, Voice, Email) are logged to console only. No actual messages will be sent.
```

### Sidebar Indicator

The sidebar shows a test mode indicator:

```
🧪 TEST MODE ACTIVE
Messages are logged, not sent
```

## Console Output Examples

### WhatsApp Message

```
============================================================
📱 WhatsApp Message (Test Mode)
============================================================
To: whatsapp:+1234567890
Time: 2024-01-15 10:30:45
Message:
🔔 Task Reminder

Task: Install POS System
Priority: HIGH
Due Date: 2024-01-20 15:00

Please update the status once completed.
============================================================
```

### Voice Call

```
============================================================
📞 Voice Call (Test Mode)
============================================================
To: John Doe (+1234567890)
Time: 2024-01-15 10:30:45
Store: Downtown Tech Hub
Task: Install POS System
Days Overdue: 3
Escalation Level: 1

Call Script:
- Hello John Doe, this is the Store Opening AI System
- URGENT escalation
- Task for Downtown Tech Hub is 3 days overdue
- Task: Install POS System
- Please take immediate action
============================================================
```

### Email Notification

```
============================================================
📧 Email (Test Mode)
============================================================
To: team@example.com, manager@example.com
From: system@storeai.com
Time: 2024-01-15 10:30:45
Subject: New Store Opening - Downtown Tech Hub

Body:
New Store Opening Notification

Store Details:
- Name: Downtown Tech Hub
- Location: New York, NY
- Opening Date: 2024-02-20
...
============================================================
```

### SMS Message

```
============================================================
📱 SMS Message (Test Mode)
============================================================
To: +1234567890
Time: 2024-01-15 10:30:45
Message:
URGENT: Task "Install POS System" is 3 days overdue for Downtown Tech Hub. Please complete immediately.
============================================================
```

## Testing Workflow

### 1. Send a WhatsApp Message

1. Navigate to **Communications** page
2. Expand any WhatsApp group
3. Type a message in the text area
4. Click **📨 Send Message**
5. See success message: "✅ Message sent to X members"
6. Check backend console for formatted output

### 2. Test Task Follow-ups

1. Navigate to **Tasks & Checklists**
2. Select a store
3. Mark tasks as in-progress or overdue
4. Wait for automated follow-ups (if scheduler is enabled)
5. Check console for follow-up messages

### 3. Test Store Creation

1. Navigate to **Stores** page
2. Click **➕ Add New Store**
3. Fill in store details
4. Click **Create Store**
5. Check console for welcome emails that would be sent

### 4. Test Escalations

1. Create overdue tasks
2. Wait for escalation scheduler (or trigger manually)
3. Check console for:
   - WhatsApp escalation messages
   - SMS escalations
   - Voice call scripts
   - Email notifications

## Switching to Production

When ready to deploy to production:

### 1. Update Environment Variables

```bash
# Set test mode to false
TEST_MODE=false

# Configure real Twilio credentials
TWILIO_ACCOUNT_SID=your_real_sid
TWILIO_AUTH_TOKEN=your_real_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+your_real_number

# Configure real email settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_real_email@gmail.com
SMTP_PASSWORD=your_real_app_password
FROM_EMAIL=your_real_email@gmail.com
```

### 2. Restart the Application

```bash
# Stop both backend and frontend
# Then restart them
python app.py
streamlit run frontend/dashboard.py
```

### 3. Verify Production Mode

- Test mode banner should disappear
- Messages will now be sent through real channels
- Verify first message sends successfully

## Benefits of Test Mode

✨ **No External Dependencies** - Test without Twilio or email accounts
🚀 **Faster Development** - Immediate feedback without waiting for messages
💰 **Cost Savings** - No SMS or voice call charges during development
🔒 **Privacy** - No risk of accidentally sending messages to real numbers
📝 **Better Logging** - See exactly what would be sent with full formatting
🧪 **Complete Testing** - Test every feature including escalations and workflows

## Troubleshooting

### Test Mode Banner Not Showing

- Verify `TEST_MODE=true` in your `.env` file
- Restart both backend and dashboard
- Check environment variable is loaded: `echo $TEST_MODE`

### Messages Still Showing Errors

- Even in test mode, the system will log "success"
- Check that Twilio/Email placeholders are filled in `.env`
- Ensure no quotes around `true` in `TEST_MODE=true`

### Console Output Not Visible

- Messages are logged to stdout (terminal output)
- If running as a service, check service logs
- For development, run in foreground to see output

## Best Practices

1. **Always use test mode during development**
2. **Test all features before switching to production**
3. **Keep test mode enabled for staging environments**
4. **Document any custom test scenarios**
5. **Use meaningful test data that resembles production**

## Summary

Test Mode provides a complete, risk-free environment for:
- Development and testing
- Demonstrations and training
- CI/CD pipelines
- Local development without external services

All features work identically in test mode and production mode, with the only difference being that messages are logged instead of sent.
