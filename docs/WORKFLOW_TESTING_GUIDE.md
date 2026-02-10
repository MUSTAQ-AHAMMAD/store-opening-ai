# Store Opening AI - Complete Workflow Testing Guide

## Overview
This document provides a comprehensive guide to testing the entire Store Opening AI workflow, including WhatsApp integration, email notifications, and the complete 7-stage store opening process.

## Prerequisites

1. **Backend Server Running**: `python app.py`
2. **Frontend Dashboard Running**: `streamlit run frontend/dashboard_enhanced.py`
3. **Environment Variables Configured**: See `.env` file
4. **Database Seeded**: Run `python data/seed_beta_data.py`

## Login Credentials

After seeding the database, use these credentials:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Manager | `manager` | `manager123` |
| Team Member | `user` | `user123` |

## Testing the Application

### 1. Login Page (FIXED - No Dark Background)

**URL**: http://localhost:8501

**What to Test**:
- Clean, light background (no dark background issue)
- Professional login form with white card
- Username and password inputs working correctly
- Login button functional

**Expected Result**:
- Light gray background (#f9fafb)
- White login card with clean borders
- All text clearly visible with dark text on light background

**Screenshot Location**: See login page at application launch

---

### 2. Dashboard Home (Main Page)

**Navigation**: After login, you're automatically on the Dashboard

**What to Test**:
- Light background on all sections
- Metric cards displaying correctly
- Store progress chart with WHITE background (not transparent/dark)
- All text readable

**Key Features to Verify**:
- **Metric Cards**: Total stores, active stores, completion rate, overdue tasks
- **Store Progress Chart**: Should have white background (`#ffffff`)
- **Upcoming Openings**: List of stores with opening dates
- **Recent Activity**: Latest updates and changes

**Expected Result**:
- All charts have white backgrounds
- No dark/transparent backgrounds visible
- Consistent light theme throughout

---

### 3. Stores Page

**Navigation**: Click "🏪 Stores" in the sidebar

**What to Test**:
- List all stores with their details
- Store creation form
- Store status updates
- Opening date management

**Stores to Test** (created by seed data):
1. Downtown Tech Hub (New York) - Opening in 15 days
2. Westside Electronics (Los Angeles) - Opening in 30 days  
3. Central Plaza Store (Chicago) - Opening in 7 days
4. Bay Area Outlet (San Francisco) - Opening in 45 days
5. Metro Center (Boston) - Completed (opened 5 days ago)

**Test Actions**:
- [ ] View all stores
- [ ] Filter by status (planning, in_progress, completed, delayed)
- [ ] Click on a store to view details
- [ ] Update store information
- [ ] Change opening date (triggers workflow recalculation)

---

### 4. Team Members Page

**Navigation**: Click "👥 Team" in the sidebar

**What to Test**:
- View all team members across stores
- Add new team member
- Assign team members to stores
- Update contact information

**Expected Data**:
- 20+ team members distributed across stores
- Multiple roles: Store Manager, IT Technician, Installation Team, Operations Lead
- Contact details (phone numbers for WhatsApp integration)

**Test Actions**:
- [ ] View team member list
- [ ] Filter by store
- [ ] Add new team member
- [ ] Update team member details
- [ ] Verify phone numbers are in WhatsApp format

---

### 5. Checklists & Tasks Page

**Navigation**: Click "✅ Tasks" in the sidebar

**What to Test**:
- View checklists for each store
- Task completion tracking
- Due dates and priorities
- Task status updates

**Checklist Categories** (per store):
1. **Hardware Setup**: POS systems, printers, scanners, cameras, network equipment
2. **Software & Accounts**: Employee accounts, inventory software, POS configuration
3. **Connectivity**: Internet setup, SIM cards, WiFi, payment gateway
4. **Training & Documentation**: Staff training, manuals, security protocols

**Test Actions**:
- [ ] View tasks for a specific store
- [ ] Mark tasks as complete
- [ ] Update task status and notes
- [ ] Check overdue tasks highlighting
- [ ] Verify priority levels (high, medium, low)

---

### 6. WhatsApp Groups Page

**Navigation**: Click "💬 WhatsApp" in the sidebar

**What to Test**:
- View WhatsApp groups for each store
- Group member management
- Send messages to groups
- View archived conversations

**WhatsApp Integration Features**:

#### 6.1 Group Structure
Each store has a dedicated WhatsApp group:
- Group name format: `Store Opening - [Store Name]`
- Members: All team members assigned to that store
- Purpose: Real-time communication and updates

#### 6.2 Automated Messages
The system sends automated WhatsApp messages for:

**Stage Notifications**:
- Stage 1: Nearby store details needed
- Stage 2: Checklist completion reminder
- Stage 3: Material arrival at nearby store
- Stage 4: Material arrival at actual store
- Stage 5: Installation start + TeamViewer ID required
- Stage 6: Final checklist reminder
- Stage 7: Store opening complete notification

**Example WhatsApp Message Flow**:

```
📍 Stage 1 - Nearby Store Details Required
------------------------------------------
Store: Downtown Tech Hub
Due: February 20, 2026

Action Required:
Please provide nearby store details for material shipment.

Required Information:
- Nearby store name
- Contact person
- Mobile number

Reply with updates in this group.
```

```
📦 Stage 3 - Material at Nearby Store
-------------------------------------
Store: Downtown Tech Hub
Update: Materials have arrived at the nearby store

Next Steps:
1. Verify all items received
2. Check for any damages
3. Confirm receipt in the system
4. Prepare for transport to actual store location

Questions? Reply in this group.
```

```
🔧 Stage 5 - Installation Starting
----------------------------------
Store: Downtown Tech Hub
Date: Opening Day - 1

IMPORTANT: TeamViewer ID Required
Before starting installation, please provide:
- TeamViewer ID for remote support
- Installation start time
- Team member names present

This is MANDATORY for remote assistance.
```

#### 6.3 Manual Messages
Users can send custom messages to groups:
- Store updates
- Schedule changes
- Emergency notifications
- General communications

**Test Actions**:
- [ ] View WhatsApp groups list
- [ ] Click on a group to see details
- [ ] View group members
- [ ] Send a test message (requires Twilio setup)
- [ ] Check archived conversations (for completed stores)

---

### 7. Workflow Management (7-Stage Process)

**Navigation**: Click "🔄 Workflow" in the sidebar

**The 7-Stage Process**:

#### Stage 1: Update Nearby Store Details (20 days before)
**Purpose**: Identify nearby store for material staging
**Required Information**:
- Nearby store name
- Contact person
- Mobile number

**Test Actions**:
- [ ] Select a store in workflow stage 1
- [ ] Fill in nearby store details
- [ ] Submit and verify stage completion
- [ ] Check WhatsApp notification sent
- [ ] Verify email notification sent

#### Stage 2: Complete Checklist & Send to Warehouse (18 days before)
**Purpose**: Finalize requirements and request materials
**Required Actions**:
- Complete all checklist items
- Verify material list
- Send request to warehouse

**Test Actions**:
- [ ] View checklist for store
- [ ] Mark all items as complete
- [ ] Submit warehouse request
- [ ] Check notification to warehouse team
- [ ] Verify stage transition

#### Stage 3: Confirm Material at Nearby Store (15 days before)
**Purpose**: Verify materials arrived at nearby location
**Required Actions**:
- Same team member confirms arrival
- Check material condition
- Verify quantities

**Test Actions**:
- [ ] View material tracking
- [ ] Confirm receipt at nearby store
- [ ] Upload any photos/notes
- [ ] Check notifications sent
- [ ] Verify timeline update

#### Stage 4: Confirm Material at Actual Store (12 days before)
**Purpose**: Verify materials transported to final location
**Required Actions**:
- Confirm arrival at store site
- Final material verification
- Ready for installation

**Test Actions**:
- [ ] Confirm material receipt
- [ ] Update material status
- [ ] Check final inventory
- [ ] Verify all team notified

#### Stage 5: Start Installation & TeamViewer ID (1 day before/opening day)
**Purpose**: Begin installation with remote support capability
**MANDATORY Requirement**:
- **TeamViewer ID** must be provided before proceeding
- Installation team contact
- Start time confirmation

**Test Actions**:
- [ ] Enter TeamViewer ID (REQUIRED)
- [ ] Provide installation team details
- [ ] Start installation process
- [ ] Test remote support connection
- [ ] Update progress notes
- [ ] Check WhatsApp group for updates

#### Stage 6: Final Checklist (Opening day)
**Purpose**: Complete final verification before opening
**Required Actions**:
- Verify all systems operational
- Test POS and payment systems
- Confirm staff trained and ready
- Final safety check

**Test Actions**:
- [ ] Complete final checklist items
- [ ] Test all equipment
- [ ] Verify staff readiness
- [ ] Submit final approval

#### Stage 7: Store Opening Complete (Opening day)
**Purpose**: Mark store as successfully opened
**Actions**:
- Store marked as complete
- Success notifications sent to all
- Historical data archived
- Group conversations archived

**Test Actions**:
- [ ] Mark store as complete
- [ ] Verify success notifications
- [ ] Check group archived
- [ ] Review completion reports

---

### 8. Analytics & Reports

**Navigation**: Click "📊 Analytics" in the sidebar

**What to Test**:
- Dashboard overview metrics
- Store progress reports
- Task completion trends
- Risk assessment
- Timeline adherence

**Key Metrics**:
- Overall completion rate
- On-time opening percentage
- Average task completion time
- Team performance metrics
- Store comparison charts

**Test Actions**:
- [ ] View dashboard analytics
- [ ] Generate store progress report
- [ ] Check task completion trends
- [ ] Review risk assessments
- [ ] Export data for offline analysis

---

### 9. AI Insights

**Navigation**: Click "🤖 AI Insights" in the sidebar

**What to Test**:
- Completion date predictions
- Task prioritization recommendations
- Risk assessment
- Intelligent follow-up suggestions

**Features**:
- **Completion Prediction**: AI predicts if store will open on time
- **Task Prioritization**: AI recommends which tasks to focus on
- **Risk Assessment**: AI identifies potential delays and risks
- **Smart Follow-ups**: AI generates context-aware messages

**Test Actions**:
- [ ] Select a store for AI analysis
- [ ] View completion prediction
- [ ] Check task priority recommendations
- [ ] Review risk assessment
- [ ] Generate AI follow-up message

---

## WhatsApp Communication Flow - Complete Example

### Scenario: New Store Opening - "Downtown Tech Hub"

**Timeline**: 20 days before opening to opening day

#### Day 1 (20 days before opening)
```
🏢 New Store Opening - Downtown Tech Hub
----------------------------------------
Store Location: New York, NY
Opening Date: February 25, 2026
Team Assigned: 5 members

Welcome to the team! This group will be used for all
communications regarding this store opening.

Your WhatsApp group is now active.
```

#### Day 3 (18 days before)
```
📍 Reminder: Nearby Store Details Needed
----------------------------------------
Hi Team,

We need to finalize the nearby store details for
material shipment. This is Stage 1 of our process.

Required by: February 15, 2026

Please provide:
- Nearby store name
- Contact person
- Contact number

Reply here or update in the system.
```

#### Day 5 (After Stage 1 Complete)
```
✅ Stage 1 Complete - Nearby Store Updated
------------------------------------------
Great job! Nearby store details confirmed:

Store: Manhattan Electronics Center
Contact: John Smith  
Number: +1-212-555-0100

Next Stage: Complete checklist and send to warehouse
Due: February 17, 2026
```

#### Day 10 (After Stage 2)
```
📦 Stage 2 Complete - Warehouse Notified
-----------------------------------------
Checklist completed and sent to warehouse!

Materials requested:
- 5 POS terminals
- 3 thermal printers
- 2 barcode scanners
- 10 security cameras
- Network equipment

Expected delivery to nearby store: February 18, 2026
```

#### Day 15 (Stage 3)
```
🚚 Material Arrival Expected
-----------------------------
Materials scheduled to arrive at nearby store today.

@SamJohnson - Please confirm receipt and verify
all items are in good condition.

Reply with confirmation once verified.
```

#### Day 18 (Stage 4)
```
📍 Material Ready for Transport
--------------------------------
Materials at nearby store verified and ready.

Next: Transport to actual store location
Expected: February 23, 2026

Team members for transport: 
@MikeWilson @SarahConnor
```

#### Day 19 (Stage 5 - Critical)
```
🔧 URGENT: Installation Starts Tomorrow
----------------------------------------
Installation begins: February 24, 2026 at 9:00 AM

⚠️ MANDATORY REQUIREMENT:
Please provide TeamViewer ID before starting.

This is required for remote support during installation.

Installation Team:
- @MikeWilson (Lead Technician)
- @TomAnderson (IT Specialist)

Reply with TeamViewer ID ASAP.
```

#### Day 20 (Opening Day - Morning)
```
🎯 Final Checklist - Opening Day
---------------------------------
Good morning team! Today's the big day!

Final checks before opening:
✅ All POS systems tested
✅ Network connectivity verified
✅ Security cameras operational
✅ Staff trained and ready
⏳ Final safety inspection - In Progress

Opening time: 10:00 AM
```

#### Day 20 (After Opening)
```
🎉 CONGRATULATIONS! Store Opening Complete
-------------------------------------------
Downtown Tech Hub is now officially open!

Opening time: 10:00 AM
Status: Success - On Time

Thank you all for your hard work and dedication!

Final metrics:
- Total tasks: 45
- Completed on time: 45
- Opening day: Exactly as scheduled
- Customer feedback: Excellent

This group will now be archived for records.
Historical data preserved.

Great job, everyone! 🎊
```

---

## Escalation Flow (For Delayed Tasks)

### Level 1: WhatsApp Reminder (1-2 days overdue)
```
⚠️ Task Overdue - Reminder
--------------------------
Task: Install POS Terminal
Assigned: @MikeWilson
Due: February 20, 2026
Status: 2 days overdue

Please provide an update on this task.
```

### Level 2: SMS + WhatsApp (3-5 days overdue)
```
🚨 URGENT: Critical Task Overdue
---------------------------------
Task: Install POS Terminal  
Days Overdue: 4
Impact: May delay store opening

This is escalated to Level 2.

Please respond immediately with:
1. Current status
2. Expected completion date
3. Any blockers/issues

Contact: Store Manager immediately if assistance needed.
```

### Level 3: Voice Call + Email + WhatsApp (7+ days overdue)
```
🔴 CRITICAL ESCALATION - Level 3
---------------------------------
Task: Install POS Terminal
Days Overdue: 7
Store Opening: At Risk

IMMEDIATE ACTIONS:
- Voice call initiated to @MikeWilson
- Email sent to store manager
- Upper management notified

This requires immediate resolution.
Store opening may need to be rescheduled.

Emergency contact: [Manager Phone]
```

---

## Email Notification Examples

### Stage Completion Email
```
Subject: ✅ Stage 2 Complete - Downtown Tech Hub

Dear Team,

Great news! Stage 2 (Checklist Completion & Warehouse Request) 
has been successfully completed for Downtown Tech Hub.

Store Details:
- Name: Downtown Tech Hub
- Location: New York, NY
- Opening Date: February 25, 2026
- Current Stage: 2 of 7

Next Stage:
Stage 3: Confirm Material at Nearby Store
Due: February 18, 2026

Materials Requested:
- 5 POS terminals
- 3 thermal printers
- [... full list ...]

Please ensure the next stage is completed on schedule.

Dashboard: http://localhost:8501

Best regards,
Store Opening AI System
```

---

## Testing Checklist - Complete Workflow

### Initial Setup
- [ ] Backend server running (http://localhost:5000)
- [ ] Frontend dashboard running (http://localhost:8501)
- [ ] Database seeded with test data
- [ ] Environment variables configured
- [ ] Twilio WhatsApp sandbox configured (optional)
- [ ] Email SMTP configured (optional)

### UI/UX Testing
- [ ] Login page - light background, no dark issues
- [ ] Dashboard home - white chart backgrounds
- [ ] All internal pages - consistent light theme
- [ ] Stores page - readable, professional design
- [ ] Team page - clean layout
- [ ] Tasks page - clear status indicators
- [ ] WhatsApp page - group list and details
- [ ] Analytics - charts with white backgrounds
- [ ] AI Insights - predictions visible

### Workflow Testing (Per Store)
- [ ] Stage 1: Nearby store details submission
- [ ] Stage 2: Checklist completion and warehouse notification
- [ ] Stage 3: Material confirmation at nearby store
- [ ] Stage 4: Material confirmation at actual store  
- [ ] Stage 5: Installation start with TeamViewer ID (MANDATORY)
- [ ] Stage 6: Final checklist completion
- [ ] Stage 7: Store opening marked complete

### WhatsApp Integration (If configured)
- [ ] Group creation for new store
- [ ] Member addition to groups
- [ ] Automated stage notifications sent
- [ ] Manual messages sent successfully
- [ ] Group archival after completion
- [ ] Escalation messages for overdue tasks

### Email Integration (If configured)
- [ ] Stage completion emails sent
- [ ] Task assignment emails sent
- [ ] Escalation emails for delays
- [ ] Daily summary emails sent
- [ ] HTML email formatting correct

### Timeline & Deadline Management
- [ ] Opening date change recalculates all stages
- [ ] Automatic deadline calculations correct
- [ ] Stage due dates update dynamically
- [ ] Overdue detection working
- [ ] Timeline visualization accurate

### Escalation Testing
- [ ] Level 0: Normal reminders (approaching due date)
- [ ] Level 1: First escalation (3+ days overdue)
- [ ] Level 2: Critical escalation (7+ days overdue)
- [ ] Multi-channel escalation (WhatsApp → SMS → Call → Email)

### Analytics & Reporting
- [ ] Dashboard metrics accurate
- [ ] Store progress calculation correct
- [ ] Task completion percentage accurate
- [ ] Risk assessment identifies issues
- [ ] Export functionality works

### AI Features (If OpenAI API configured)
- [ ] Completion prediction generated
- [ ] Task prioritization recommendations
- [ ] Risk assessment AI insights
- [ ] AI-generated follow-up messages

---

## Production Readiness Checklist

### Security
- [ ] Change default passwords
- [ ] Use strong SECRET_KEY in production
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Use production database (PostgreSQL)
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Sanitize user inputs
- [ ] Secure file uploads

### Performance
- [ ] Database indexed properly
- [ ] API response caching implemented
- [ ] Large dataset pagination working
- [ ] Chart rendering optimized
- [ ] Lazy loading for heavy components

### Monitoring
- [ ] Application logging configured
- [ ] Error tracking setup
- [ ] Performance monitoring
- [ ] API health checks
- [ ] Database backup strategy

### Deployment
- [ ] Use production WSGI server (Gunicorn)
- [ ] Configure reverse proxy (Nginx)
- [ ] Setup SSL certificates
- [ ] Environment variables secured
- [ ] Database migrations strategy
- [ ] Backup and recovery plan
- [ ] Monitoring and alerting setup

---

## Troubleshooting

### Issue: Dark Background on Internal Pages
**Solution**: Updated chart backgrounds from `rgba(0,0,0,0)` to `#ffffff` in `dashboard_enhanced.py` line 1021-1022

### Issue: Login Not Working
**Verify**:
1. Backend server is running
2. Database is seeded
3. Credentials are correct
4. No CORS errors in browser console

### Issue: WhatsApp Messages Not Sending
**Verify**:
1. Twilio credentials in `.env`
2. WhatsApp sandbox joined
3. Phone numbers in correct format (whatsapp:+1...)
4. Twilio account has balance

### Issue: Emails Not Sending
**Verify**:
1. SMTP settings in `.env`
2. App password for Gmail (not regular password)
3. Port 587 accessible
4. FROM_EMAIL matches SMTP_USER

---

## Support

For issues or questions:
1. Check this documentation
2. Review application logs
3. Check API health: http://localhost:5000/health
4. Open GitHub issue with details

---

**Last Updated**: February 10, 2026
**Version**: 3.0
**Author**: Store Opening AI Team
