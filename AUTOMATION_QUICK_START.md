# Process Automation - Quick Start Guide

## ✅ YES! This System Handles Complete Process Automation

This guide shows you how to get the complete automation system running in **5 minutes**.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install & Configure (2 minutes)

```bash
# Clone the repository
git clone https://github.com/MUSTAQ-AHAMMAD/store-opening-ai.git
cd store-opening-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (use TEST MODE to start)
cp .env.example .env
```

### Step 2: Enable Test Mode (30 seconds)

Edit `.env` file and set:

```bash
# Enable Test Mode - No external services required!
TEST_MODE=true

# Enable automated schedulers
ENABLE_SCHEDULER=true
SCHEDULER_TIMEZONE=UTC
```

**That's it!** You don't need Twilio, OpenAI, or email accounts in test mode.

### Step 3: Initialize Database (1 minute)

```bash
# Create database and seed with sample data
python data/seed_beta_data.py
```

This creates:
- ✅ 5 sample stores with different opening dates
- ✅ 7 workflow stages for each store
- ✅ 20+ team members
- ✅ Complete checklists with tasks
- ✅ Default user accounts (admin/admin123, manager/manager123, user/user123)

### Step 4: Start the Automation (1 minute)

```bash
# Terminal 1: Start Backend (includes ALL automation)
python main.py
```

```bash
# Terminal 2: Start Dashboard
streamlit run frontend/dashboard.py
```

### Step 5: Verify Automation is Running (30 seconds)

Open your browser to:
- **Backend API:** http://localhost:5000
- **Dashboard:** http://localhost:8501

**Login with:** 
- Username: `admin`
- Password: `admin123`

---

## 🎉 What Just Happened?

Your system is now running with **FULL AUTOMATION**:

### ✅ Active Background Schedulers

1. **Hourly Follow-up Check** - Sends pending follow-up messages
2. **2-Hour Workflow Monitor** - Checks for delayed workflow stages
3. **6-Hour Task Monitor** - Detects overdue tasks and escalates
4. **Daily Summary** (9 AM) - Sends progress summaries to team

### ✅ Automatic Workflow Processes

- **7-Stage Sequential Workflow** - Auto-advances stages
- **Timeline Recalculation** - Updates all deadlines when opening date changes
- **Material Tracking** - 4-checkpoint automated logistics
- **TeamViewer Integration** - Remote support automation

### ✅ Multi-Channel Notifications

In test mode, you'll see console output like:

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

============================================================
📞 Voice Call (Test Mode)
============================================================
To: John Doe (+1234567890)
Store: Downtown Tech Hub
Task: Install POS System
Days Overdue: 3
Escalation Level: 1

Call Script:
- Hello John Doe, this is the Store Opening AI System
- URGENT escalation for Downtown Tech Hub
- Task "Install POS System" is 3 days overdue
- Please take immediate action
============================================================
```

### ✅ AI & ML Features

- **AI-Powered Messages** - Context-aware follow-ups
- **Risk Assessment** - Predicts completion probability
- **Task Prioritization** - AI suggests optimal task order
- **Self-Learning Models** - 4 ML models that improve over time

---

## 📊 Test the Automation

### Test 1: Workflow Auto-Advancement

```bash
# API call to complete Stage 1
curl -X POST http://localhost:5000/api/workflow/store/1/nearby-store \
  -H "Content-Type: application/json" \
  -d '{
    "store_name": "Nearby Store",
    "store_address": "123 Main St",
    "contact_person_name": "John Doe",
    "contact_person_mobile": "+1234567890",
    "distance_km": 5.0,
    "updated_by_id": 1
  }'
```

**Expected Result:** 
- ✅ Stage 1 marked as completed
- ✅ Stage 2 automatically started
- ✅ Notifications sent (in test mode: logged to console)

### Test 2: Timeline Recalculation

```bash
# Change opening date
curl -X PUT http://localhost:5000/api/workflow/store/1/opening-date \
  -H "Content-Type: application/json" \
  -d '{
    "opening_date": "2024-06-01T00:00:00Z"
  }'
```

**Expected Result:**
- ✅ All stage due dates recalculated
- ✅ Notifications sent about timeline change
- ✅ Console shows WhatsApp and Email notifications (test mode)

### Test 3: ML Predictions

```bash
# Get risk assessment
curl http://localhost:5000/api/ml/assess/risk/1
```

**Expected Result:**
```json
{
  "store_id": 1,
  "risk_level": "medium",
  "risk_score": 45,
  "predictions": {
    "completion_probability": 0.78,
    "on_time_likelihood": "medium",
    "days_difference": 2
  },
  "recommendations": [
    "Monitor high-priority tasks closely",
    "Consider adding team resources"
  ]
}
```

### Test 4: AI Message Generation

```bash
# Generate AI follow-up for a task
curl -X POST http://localhost:5000/api/ai/task/1/generate-followup
```

**Expected Result:** AI-generated context-aware message

---

## 🔧 Configure for Production

When ready to use real services:

### 1. Get Twilio Account (for WhatsApp, SMS, Voice)

```bash
# Sign up at twilio.com
# Get your credentials and update .env:

TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+1234567890
```

### 2. Configure Email (SMTP)

```bash
# For Gmail:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password  # Create app password in Gmail settings
FROM_EMAIL=your_email@gmail.com
```

### 3. Add OpenAI (Optional, for AI features)

```bash
OPENAI_API_KEY=sk-your-openai-api-key
```

### 4. Disable Test Mode

```bash
TEST_MODE=false
```

### 5. Restart the Application

```bash
python main.py
```

Now all notifications will be sent through real channels!

---

## 📚 Available Automation Endpoints

### Workflow Automation

```bash
# Get all workflow stages
GET /api/workflow/store/{id}/stages

# Complete stages
POST /api/workflow/store/{id}/nearby-store      # Stage 1
POST /api/workflow/store/{id}/warehouse-shipment # Stage 2
POST /api/workflow/store/{id}/nearby-store-receipt # Stage 3
POST /api/workflow/store/{id}/store-receipt      # Stage 4
POST /api/workflow/store/{id}/installation       # Stage 5
POST /api/workflow/store/{id}/final-checklist    # Stage 6
POST /api/workflow/store/{id}/complete           # Stage 7

# Update opening date (triggers timeline recalc)
PUT /api/workflow/store/{id}/opening-date

# Get delayed stages
GET /api/workflow/store/{id}/delayed-stages

# Get escalation history
GET /api/workflow/store/{id}/escalations

# Material tracking
GET /api/workflow/store/{id}/material-tracking
```

### AI & ML Automation

```bash
# AI-powered features
POST /api/ai/task/{id}/generate-followup
GET  /api/ai/task/{id}/risk-assessment
GET  /api/ai/store/{id}/task-prioritization
GET  /api/ai/insights/dashboard
GET  /api/ai/predict/completion-date/{store_id}

# ML predictions
POST /api/ml/learn/store/{id}           # Train from completed store
GET  /api/ml/predict/success/{id}       # Success probability
GET  /api/ml/assess/risk/{id}           # Risk assessment
GET  /api/ml/predict/duration/{task_id} # Task duration
GET  /api/ml/analyze/success-factors/{id} # Success patterns
GET  /api/ml/stats                      # Model statistics
```

### Voice & Escalations

```bash
# Voice calling
POST /api/voice/escalate/task/{id}
POST /api/voice/escalate/manager/{id}
GET  /api/voice/call-status/{call_sid}
POST /api/voice/test-call
```

---

## 🧪 Testing Automation

Run the automation test suite:

```bash
# Run all automation tests
python -m pytest test_automation_capabilities.py -v

# Run specific test category
python -m pytest test_automation_capabilities.py::TestWorkflowAutomation -v
python -m pytest test_automation_capabilities.py::TestMLLearning -v
python -m pytest test_automation_capabilities.py::TestNotificationAutomation -v
```

---

## 📊 Monitor Automation

### Check Scheduler Status

The scheduler logs show when jobs run:

```
Follow-up scheduler started
[2024-01-15 10:00:00] Running job: check_follow_ups
Processed 5 follow-ups
[2024-01-15 12:00:00] Running job: check_workflow_delays
Checked 10 stores, found 2 delays
[2024-01-15 16:00:00] Running job: check_overdue_tasks
Found 3 overdue tasks, sent escalations
```

### View Escalation History

```bash
# Get escalations for a store
curl http://localhost:5000/api/workflow/store/1/escalations
```

### Check ML Model Stats

```bash
# Get ML model training statistics
curl http://localhost:5000/api/ml/stats
```

---

## 🎯 Automation Best Practices

### 1. Start in Test Mode
Always start in test mode to verify automation without sending real messages.

### 2. Monitor Logs
Keep an eye on console output to see automation activity.

### 3. Configure Timezones
Set `SCHEDULER_TIMEZONE` to your local timezone for daily summaries.

### 4. Batch Learning
After completing multiple stores, run batch learning:

```bash
curl -X POST http://localhost:5000/api/ml/learn/batch \
  -H "Content-Type: application/json" \
  -d '{"store_ids": [1, 2, 3, 4, 5]}'
```

### 5. Review ML Predictions
Regularly check model accuracy and retrain if needed.

---

## 🔍 Troubleshooting Automation

### Scheduler Not Running

```bash
# Check ENABLE_SCHEDULER in .env
ENABLE_SCHEDULER=true

# Restart the application
python main.py
```

### Messages Not Sending (Production Mode)

```bash
# Check TEST_MODE is disabled
TEST_MODE=false

# Verify Twilio credentials
# Check account balance
# Confirm phone numbers are in E.164 format (+1234567890)
```

### ML Models Not Predicting

```bash
# Models need minimum 10 samples
# Train from completed stores:
curl -X POST http://localhost:5000/api/ml/learn/store/1

# Check model stats:
curl http://localhost:5000/api/ml/stats
```

### Workflow Stages Not Advancing

```bash
# Ensure previous stage is completed
# Check due dates are set correctly
# Verify team member IDs are valid
```

---

## 📖 Further Reading

- [PROCESS_AUTOMATION_CAPABILITIES.md](./PROCESS_AUTOMATION_CAPABILITIES.md) - Complete automation reference
- [WORKFLOW_AUTOMATION.md](./docs/WORKFLOW_AUTOMATION.md) - Detailed workflow guide
- [ML_ADMINLTE_GUIDE.md](./ML_ADMINLTE_GUIDE.md) - ML features guide
- [TEST_MODE_GUIDE.md](./TEST_MODE_GUIDE.md) - Test mode documentation
- [API_DOCUMENTATION.md](./docs/API_DOCUMENTATION.md) - All API endpoints

---

## ✅ Success Checklist

After following this guide, you should have:

- [x] System running with all automation active
- [x] 4 background schedulers monitoring continuously
- [x] 7-stage workflow automation working
- [x] Multi-channel notifications configured
- [x] AI & ML features operational
- [x] Test mode validating automation works
- [x] Understanding of all automation capabilities

---

## 🎉 You're Ready!

Your Store Opening AI system is now fully automated and ready to:

- ✅ Manage store opening workflows automatically
- ✅ Send intelligent escalations and follow-ups
- ✅ Track materials from warehouse to store
- ✅ Predict risks and suggest optimizations
- ✅ Learn and improve from every completed store
- ✅ Scale to hundreds of simultaneous store openings

**Questions?** Check the documentation or create an issue on GitHub.

---

**Built with ❤️ for complete process automation**
