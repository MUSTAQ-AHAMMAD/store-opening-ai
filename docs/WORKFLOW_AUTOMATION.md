# Store Opening Workflow Automation - Complete Guide

## Overview

This system implements a comprehensive 7-stage workflow automation for store opening management with AI-powered follow-ups, multi-channel escalations, and automatic timeline management.

## 7-Stage Workflow Process

### Stage 1: Update Nearby Store Details
**Timeline:** 20 days before opening  
**Responsible:** Team Member  
**Task:** Update nearby store details including:
- Store name and address
- Contact person name
- Contact person mobile number
- Distance from new store

**API Endpoint:**
```bash
POST /api/workflow/store/{store_id}/nearby-store
{
  "store_name": "ABC Store",
  "store_address": "123 Main St",
  "contact_person_name": "John Doe",
  "contact_person_mobile": "+1234567890",
  "distance_km": 5.5,
  "updated_by_id": 1
}
```

### Stage 2: Complete Checklist & Send to Warehouse
**Timeline:** 18 days before opening  
**Responsible:** Team  
**Task:** 
- Complete all checklist items
- Send material requirements to warehouse
- Warehouse prepares shipment

**API Endpoint:**
```bash
POST /api/workflow/store/{store_id}/warehouse-shipment
{
  "confirmed_by_id": 1
}
```

**Notifications:**
- Person who updated nearby store details is notified
- WhatsApp group receives update
- Email sent to team

### Stage 3: Confirm Material Reached Nearby Store
**Timeline:** 15 days before opening  
**Responsible:** Same team member from Stage 1  
**Task:** Confirm material shipment arrived at nearby store

**API Endpoint:**
```bash
POST /api/workflow/store/{store_id}/nearby-store-receipt
{
  "confirmed_by_id": 1
}
```

### Stage 4: Confirm Material Sent to Actual Store
**Timeline:** 12 days before opening  
**Responsible:** Same team member  
**Task:** Confirm material transported from nearby store to actual store location

**API Endpoint:**
```bash
POST /api/workflow/store/{store_id}/store-receipt
{
  "confirmed_by_id": 1
}
```

### Stage 5: Start Installation & Update TeamViewer ID
**Timeline:** 1 day before opening or on opening day  
**Responsible:** Installation Technician  
**Task:** 
- Start installation process
- Update TeamViewer ID (MANDATORY)
- Enable remote support

**API Endpoint:**
```bash
POST /api/workflow/store/{store_id}/installation
{
  "teamviewer_id": "123456789",
  "technician_id": 1
}
```

**Why TeamViewer ID is Mandatory:**
- Enables remote support during installation
- Allows technical team to assist without being on-site
- Faster issue resolution
- Better documentation of installation process

### Stage 6: Complete Final Checklist on Opening Day
**Timeline:** Opening day  
**Responsible:** Same team member  
**Task:** 
- Verify all installations complete
- Check all systems operational
- Final quality check

**API Endpoint:**
```bash
POST /api/workflow/store/{store_id}/final-checklist
{
  "completed_by_id": 1
}
```

### Stage 7: Store Opening Complete
**Timeline:** Opening day  
**Status:** Automated  
**Task:** System marks store opening as complete

**API Endpoint:**
```bash
POST /api/workflow/store/{store_id}/complete
```

## Automatic Features

### 1. Timeline Recalculation
When opening date changes, all stage deadlines are automatically recalculated:

```bash
PUT /api/workflow/store/{store_id}/opening-date
{
  "opening_date": "2024-05-15T00:00:00Z"
}
```

**What Happens:**
- All incomplete stage deadlines are recalculated
- WhatsApp group notified with new deadlines
- Email sent to all team members
- Timeline adjustments based on days before opening

### 2. Multi-Channel Escalations

#### Escalation Levels Based on Delay:
- **1 day overdue:** WhatsApp reminder
- **2 days overdue:** WhatsApp + SMS
- **3 days overdue:** WhatsApp + SMS + Voice Call
- **5+ days overdue:** All channels + Email to Manager

#### Escalation Channels:
1. **WhatsApp:** Instant messaging to team member
2. **SMS:** Text message alert
3. **Voice Call:** Automated phone call
4. **Email:** Formal escalation to manager

### 3. AI-Powered Messages

The system uses AI (OpenAI GPT) to generate:
- Contextual follow-up messages
- Professional escalation emails
- Personalized reminders based on:
  - Days overdue
  - Priority level
  - Store opening timeline
  - Overall project progress
  - Team member role

### 4. Automated Scheduler Jobs

#### Every Hour:
- Check pending follow-ups
- Send scheduled reminders

#### Every 2 Hours:
- **Check workflow stage delays**
- Escalate delayed stages
- Notify managers of critical delays

#### Every 6 Hours:
- Check overdue tasks
- Send escalations with AI-generated messages
- Make voice calls for critical delays

#### Daily at 9 AM:
- Send daily summary to all team members
- Include progress statistics
- Highlight overdue items

## Communication Flow

### WhatsApp Group
All workflow updates are broadcast to the WhatsApp group:
- Stage completions
- Stage starts
- Material tracking updates
- Delay notifications
- Opening date changes

### Email Notifications
Sent for:
- New store creation (with workflow overview)
- Stage transitions
- Manager escalations
- Opening date changes

### SMS Notifications
Sent for:
- High-priority delays
- Urgent escalations

### Voice Calls
Made for:
- Critical delays (3+ days overdue)
- Emergency escalations to managers

## API Endpoints Reference

### Workflow Management
- `GET /api/workflow/store/{store_id}/stages` - Get all workflow stages
- `GET /api/workflow/store/{store_id}/stages/{stage_number}` - Get specific stage
- `GET /api/workflow/store/{store_id}/delayed-stages` - Get delayed stages
- `GET /api/workflow/store/{store_id}/escalations` - Get escalation history

### Material Tracking
- `GET /api/workflow/store/{store_id}/material-tracking` - Get material status
- `GET /api/workflow/store/{store_id}/nearby-store` - Get nearby store details

### Installation
- `GET /api/workflow/store/{store_id}/installation` - Get TeamViewer details
- `PUT /api/workflow/store/{store_id}/installation` - Update installation notes

### Store Management
- `PUT /api/workflow/store/{store_id}/opening-date` - Update opening date

## Configuration

### Environment Variables

```bash
# Email Configuration (required for email notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com

# Twilio Configuration (required for WhatsApp, SMS, Voice)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+1234567890

# OpenAI Configuration (optional, for AI-powered messages)
OPENAI_API_KEY=your_openai_api_key

# Scheduler Configuration
ENABLE_SCHEDULER=true
SCHEDULER_TIMEZONE=UTC
```

### Gmail Setup for Email
1. Enable 2-factor authentication
2. Generate app password
3. Use app password in `SMTP_PASSWORD`

### Twilio Setup
1. Create Twilio account
2. Get Account SID and Auth Token
3. Set up WhatsApp sandbox (development)
4. Apply for WhatsApp Business API (production)

## Database Models

### New Models Added:
- `NearbyStoreDetails` - Stores nearby store information
- `MaterialTracking` - Tracks material movement
- `TeamViewerSession` - Stores remote support details
- `WorkflowStage` - Tracks each of the 7 stages
- `EscalationHistory` - Logs all escalations

### Updated Models:
- `Store` - Added `workflow_stage` field

## Best Practices

1. **Always Update TeamViewer ID**: This is mandatory for remote support

2. **Assign Consistent Team Member**: The same person should handle stages 1, 3, 4, 5, and 6 for continuity

3. **Monitor Escalations**: Managers should respond quickly to escalation notifications

4. **Update Opening Date Early**: If date changes, update immediately to recalculate timelines

5. **Use WhatsApp Group**: All communication should happen in the group for transparency

6. **Document Progress**: Use the notes field when advancing stages

## Troubleshooting

### Emails Not Sending
- Check SMTP credentials in `.env`
- Verify Gmail app password
- Check firewall settings

### WhatsApp Messages Not Sending
- Verify Twilio credentials
- Check account balance
- Ensure numbers are in E.164 format

### Voice Calls Not Working
- Ensure `TWILIO_PHONE_NUMBER` is configured
- Verify phone number is verified in Twilio
- Check voice service is enabled

### Stage Not Advancing
- Ensure previous stage is completed
- Check team member ID is valid
- Verify all required fields are provided

## Security Considerations

1. **Never commit `.env` file** to version control
2. **Use app passwords** for Gmail, not main password
3. **Rotate API keys** regularly
4. **Limit manager access** to escalation endpoints
5. **Validate team member permissions** before stage updates

## Support

For issues or questions:
1. Check logs in the application
2. Review escalation history
3. Contact system administrator
4. Check Twilio/OpenAI/Email service status

---

**Built with ❤️ for efficient store opening management**
