# 🧪 Local Testing Guide - Test AI Communication on Your Machine

## 📋 Overview

This guide will help you **run the Store Opening AI system on your local machine** and **test how the AI communicates** without requiring any external services (no Twilio, no OpenAI, no email accounts needed).

Perfect for:
- 🧪 Testing the system locally before production
- 🤖 Understanding how AI communication works
- 🔍 Exploring the features and workflows
- 💡 Learning the system architecture

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Prerequisites

Make sure you have:
- **Python 3.9+** installed (Python 3.12+ recommended)
- **Git** installed
- **Terminal/Command Prompt** access

**Check your Python version:**
```bash
python --version
# Should show Python 3.9 or higher
```

### Step 2: Clone and Setup

```bash
# 1. Clone the repository
git clone https://github.com/MUSTAQ-AHAMMAD/store-opening-ai.git
cd store-opening-ai

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Upgrade pip and install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Step 3: Configure Test Mode

```bash
# Copy the example environment file
cp .env.example .env
```

**Edit `.env` file and ensure these settings:**
```bash
# Enable Test Mode - NO external services needed!
TEST_MODE=true

# Enable the automation schedulers
ENABLE_SCHEDULER=true
SCHEDULER_TIMEZONE=UTC

# Flask settings
FLASK_ENV=development
SECRET_KEY=test-secret-key-change-in-production
DEBUG=true

# Database (SQLite - no setup needed)
DATABASE_URL=sqlite:///store_opening.db

# Optional: AI Features (not required for testing)
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
```

**💡 Important:** With `TEST_MODE=true`, you don't need real Twilio credentials or email settings. The system will log all messages to the console.

### Step 4: Initialize Database

```bash
# Create database tables and seed with sample data
python data/seed_beta_data.py
```

This creates:
- ✅ Database with all required tables
- ✅ 5 sample stores at different workflow stages
- ✅ 20+ team members
- ✅ Complete checklists and tasks
- ✅ Default user accounts:
  - **Admin:** username=`admin`, password=`admin123`
  - **Manager:** username=`manager`, password=`manager123`
  - **User:** username=`user`, password=`user123`

### Step 5: Start the Application

**Open TWO terminal windows:**

**Terminal 1 - Backend API:**
```bash
cd store-opening-ai
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

You should see:
```
==================================================
Store Opening AI - Backend Server
==================================================
Server running on: http://localhost:5000
Debug mode: True
Database: sqlite:///store_opening.db
==================================================
```

**Terminal 2 - Dashboard UI:**
```bash
cd store-opening-ai
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run frontend/dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

---

## 🤖 Testing AI Communication

### What is "AI Communication" in This System?

The system uses AI to:
1. **Generate intelligent follow-up messages** based on context
2. **Assess task completion risks** using historical data
3. **Predict store opening readiness** 
4. **Create personalized escalation messages** for different team members
5. **Learn from historical data** to improve predictions

### Test Mode vs Production Mode

| Feature | Test Mode | Production Mode |
|---------|-----------|-----------------|
| AI Message Generation | ✅ Logged to console | ✅ Sent via WhatsApp/SMS/Email |
| Voice Calls | ✅ Script shown in console | ✅ Actual Twilio call made |
| Email Notifications | ✅ Email content logged | ✅ Real email sent |
| SMS Messages | ✅ Message logged | ✅ Real SMS sent |
| WhatsApp Messages | ✅ Message logged | ✅ Real WhatsApp sent |
| AI Risk Assessment | ✅ Works fully | ✅ Works fully |
| ML Predictions | ✅ Works fully | ✅ Works fully |
| Workflow Automation | ✅ Works fully | ✅ Works fully |

### How to Test AI Communication (Step-by-Step)

#### 1. Login to Dashboard

1. Open `http://localhost:8501` in your browser
2. You'll see a **🧪 TEST MODE** banner (this is good!)
3. Login with: `admin` / `admin123`

#### 2. View Active Stores

- Navigate to **🏪 Stores** in the sidebar
- You'll see 5 sample stores:
  - Some are "Planning"
  - Some are "In Progress"
  - One is already "Completed"

#### 3. Test AI Follow-Up Messages

**Option A: Through the Dashboard**
1. Go to **✅ Tasks & Checklists**
2. Select a store from the dropdown
3. You'll see tasks with different statuses
4. Click "Send Follow-up" on any task
5. **Check Terminal 1** (backend) - You'll see the AI-generated message!

**Option B: Using API (Direct Testing)**
```bash
# First, get an auth token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Copy the token from the response, then:
TOKEN="paste_your_token_here"

# Generate AI follow-up for task ID 1
curl -X POST http://localhost:5000/api/ai/task/1/generate-followup \
  -H "Authorization: Bearer $TOKEN"
```

**What to Look For:**
- In Terminal 1, you'll see formatted output showing:
  - The AI-generated message
  - Task context (priority, due date, store info)
  - Recipient details
  - Message delivery method (WhatsApp/SMS/Email)

#### 4. Test AI Risk Assessment

```bash
# Get risk assessment for task ID 1
curl http://localhost:5000/api/ai/task/1/risk-assessment \
  -H "Authorization: Bearer $TOKEN"
```

**Response Example:**
```json
{
  "risk_level": "MEDIUM",
  "risk_score": 0.65,
  "factors": [
    "Task is 2 days overdue",
    "High priority task",
    "Store opening in 7 days"
  ],
  "recommendations": [
    "Escalate to team lead",
    "Consider reassigning if not resolved in 24 hours"
  ]
}
```

#### 5. Test Store Completion Prediction

```bash
# Predict completion date for store ID 1
curl http://localhost:5000/api/ai/predict/completion-date/1 \
  -H "Authorization: Bearer $TOKEN"
```

#### 6. Test Workflow Automation

**Watch the Console for Automated Actions:**

The system runs **4 background schedulers**:

1. **Hourly Follow-up Check** - Looks for pending messages
2. **2-Hour Workflow Monitor** - Checks for delayed workflow stages
3. **6-Hour Task Monitor** - Detects overdue tasks
4. **Daily Summary** (9 AM UTC) - Sends progress reports

**To see them in action:**
1. Keep Terminal 1 running
2. Create a task with a due date in the past
3. Wait a few minutes
4. Watch the console - you'll see automated escalation messages!

#### 7. Test Multi-Level Escalations

The system has a **4-level escalation system**:

- **Level 0:** Normal reminder (task approaching due date)
- **Level 1:** First escalation (3+ days overdue) → WhatsApp
- **Level 2:** Second escalation (5+ days overdue) → SMS
- **Level 3:** Critical escalation (7+ days overdue) → Voice Call
- **Level 4:** Manager escalation → Email to management

**Test Manual Escalation:**
```bash
# Escalate task 1 (Level 1)
curl -X POST http://localhost:5000/api/voice/escalate/task/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"escalation_level": 1}'
```

**Check Terminal 1** - You'll see:
- ✉️ WhatsApp message content
- 📱 SMS message content
- 📞 Voice call script (what would be spoken)
- 📧 Email content

---

## 🎯 Understanding the Console Output

### Example: WhatsApp Message in Test Mode

```
============================================================
📱 WhatsApp Message (Test Mode)
============================================================
To: whatsapp:+1234567890
Time: 2024-01-15 10:30:45
Store: Downtown Tech Hub
Task: Install POS System

Message:
🔔 Task Reminder - Action Required

Hi John Doe,

This is a friendly reminder about your task:

📋 Task: Install POS System
⭐ Priority: HIGH
📅 Due Date: 2024-01-20 15:00
⏰ Status: OVERDUE by 2 days

🏪 Store: Downtown Tech Hub
📍 Opening Date: 2024-01-25

Please update the task status as soon as possible.
The store opening is just 10 days away!

Reply 'DONE' when completed or 'HELP' if you need assistance.

Thanks,
Store Opening AI Team
============================================================
```

### Example: Voice Call Script in Test Mode

```
============================================================
📞 Voice Call (Test Mode)
============================================================
To: John Doe (+1234567890)
Time: 2024-01-15 10:30:45
Store: Downtown Tech Hub
Task: Install POS System
Days Overdue: 3
Escalation Level: 2

Call Script:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hello John Doe, this is the Store Opening AI System.

This is an URGENT escalation regarding the Downtown Tech Hub 
store opening.

Task "Install POS System" is now 3 days overdue.

This is a HIGH priority task for the store opening on 
January 25th, 2024.

Please take immediate action and update the task status.

If you need assistance, please contact your manager or 
reply to this message.

Thank you.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
============================================================
```

### Example: AI Risk Assessment Output

```
============================================================
🤖 AI Risk Assessment
============================================================
Task ID: 15
Task: "Configure Payment Gateway"
Store: Central Plaza Store
Priority: HIGH

Risk Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk Level: HIGH 🔴
Risk Score: 0.82

Contributing Factors:
• Task is 5 days overdue
• High priority task
• Store opening in 7 days (only 2 days buffer)
• Previous similar tasks took 3 days on average
• Team member has 3 other overdue tasks

Recommendations:
✓ IMMEDIATE escalation required
✓ Consider reassigning to available team member
✓ Manager notification recommended
✓ Daily check-ins until completion

Predicted Completion: 2 days (if started immediately)
Confidence: 75%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
============================================================
```

---

## 🔬 Advanced Testing Scenarios

### Scenario 1: Complete a Workflow Stage

```bash
# Get current workflow stages for store 1
curl http://localhost:5000/api/workflow/store/1/stages \
  -H "Authorization: Bearer $TOKEN"

# Complete Stage 1: Update nearby store details
curl -X POST http://localhost:5000/api/workflow/store/1/nearby-store \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nearby_store_name": "Warehouse Store #5",
    "contact_person": "Jane Smith",
    "contact_mobile": "+1234567890"
  }'

# Check Terminal 1 - you'll see:
# - WhatsApp notification to team
# - Email notification
# - Workflow stage marked complete
# - Next stage automatically activated!
```

### Scenario 2: Change Opening Date (Timeline Recalculation)

```bash
# Update store opening date
curl -X PUT http://localhost:5000/api/workflow/store/1/opening-date \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"opening_date": "2024-02-15"}'

# Watch Terminal 1 - you'll see:
# - All workflow stage deadlines recalculated
# - Team notified of new timeline
# - Tasks deadline adjusted
# - AI re-assesses risk based on new timeline
```

### Scenario 3: Material Tracking

```bash
# Track material through the logistics chain
# Stage 2: Warehouse sends materials
curl -X POST http://localhost:5000/api/workflow/store/1/warehouse-shipment \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"shipped_at": "2024-01-15T10:00:00"}'

# Stage 3: Nearby store receives materials
curl -X POST http://localhost:5000/api/workflow/store/1/nearby-store-receipt \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"received_at": "2024-01-16T14:30:00"}'

# Stage 4: Actual store receives materials
curl -X POST http://localhost:5000/api/workflow/store/1/store-receipt \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"received_at": "2024-01-17T09:00:00"}'

# Check material tracking status
curl http://localhost:5000/api/workflow/store/1/material-tracking \
  -H "Authorization: Bearer $TOKEN"
```

### Scenario 4: ML Model Training & Predictions

The system has **4 self-learning ML models**:

1. **Completion Time Predictor** - Predicts how long tasks will take
2. **Risk Classifier** - Classifies tasks by risk level
3. **Success Pattern Analyzer** - Identifies what makes stores successful
4. **Timeline Optimizer** - Suggests optimal timelines

```bash
# Get ML-powered insights
curl http://localhost:5000/api/ml/insights/dashboard \
  -H "Authorization: Bearer $TOKEN"

# Get store success probability
curl http://localhost:5000/api/ml/store/1/success-probability \
  -H "Authorization: Bearer $TOKEN"

# Get task completion time prediction
curl http://localhost:5000/api/ml/task/1/completion-prediction \
  -H "Authorization: Bearer $TOKEN"

# Train models with historical data (if available)
curl -X POST http://localhost:5000/api/ml/train \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📊 Dashboard Features to Explore

### 1. Dashboard Overview
- **Real-time Metrics:** Active stores, total tasks, completion rate
- **Risk Assessment Cards:** AI-powered risk analysis
- **Store Progress Charts:** Visual timeline tracking
- **Upcoming Deadlines:** Next 7 days preview

### 2. Store Management
- **Create New Store:** Full workflow initialization
- **View Store Details:** Complete workflow status
- **Update Store Info:** Changes trigger timeline recalculation
- **Track Progress:** Visual stage completion

### 3. Team Management
- **Team Directory:** All team members by store
- **Task Assignment:** Assign tasks to team members
- **Performance Tracking:** Task completion stats
- **Contact Information:** Phone, email, WhatsApp

### 4. Tasks & Checklists
- **Task Categories:** Hardware, Software, Connectivity, Training
- **Priority Levels:** LOW, MEDIUM, HIGH, CRITICAL
- **Status Tracking:** NOT_STARTED, IN_PROGRESS, COMPLETED
- **Bulk Operations:** Update multiple tasks at once

### 5. WhatsApp Groups
- **Group Management:** Create and manage store groups
- **Message Broadcasting:** Send to entire team
- **Conversation Archive:** Historical messages
- **Quick Templates:** Pre-written message templates

### 6. Analytics & Insights
- **Store Performance:** Success rates and timelines
- **Task Analytics:** Completion trends
- **Team Performance:** Individual and team stats
- **Risk Dashboard:** AI-powered risk visualization

### 7. Workflow Automation
- **7-Stage Process:** Visual workflow tracker
- **Stage Completion:** Mark stages complete
- **Material Tracking:** Logistics visualization
- **TeamViewer Integration:** Remote support tracking

### 8. ML & AI Features
- **Self-Learning Models:** Train on your data
- **Predictive Analytics:** Success probabilities
- **Risk Assessment:** Real-time risk scoring
- **Smart Recommendations:** AI-suggested actions

---

## 🐛 Troubleshooting

### Issue 1: Windows - "'.' is not recognized as an internal or external command"

**Problem:** Trying to run `./setup.bat` or `./start_backend.bat` on Windows

**Solution:**
On Windows Command Prompt, you cannot use the `./` prefix. Use these commands instead:

```cmd
# Correct way (without ./)
setup.bat
start_backend.bat
start_dashboard.bat

# Alternative (with backslash)
.\setup.bat
.\start_backend.bat
.\start_dashboard.bat
```

**Why?** The `./` syntax is specific to Unix/Linux/Mac shells. Windows Command Prompt uses different path conventions.

### Issue 2: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Issue 3: "Database not found" error

**Solution:**
```bash
# Re-initialize database
python data/seed_beta_data.py
```

### Issue 4: Port 5000 already in use

**Solution:**
```bash
# Option 1: Kill the process using port 5000
# On Linux/Mac:
lsof -ti:5000 | xargs kill -9
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Option 2: Use a different port
# Edit .env:
PORT=5001
# Then use: python main.py
```

### Issue 5: Dashboard won't open

**Solution:**
```bash
# Make sure backend is running first
# Check Terminal 1 shows "Server running on: http://localhost:5000"

# Try running dashboard with explicit port
streamlit run frontend/dashboard.py --server.port 8501
```

### Issue 6: AI features not working

**Solution:**
```bash
# In TEST MODE, AI features work with mock data
# To use real AI:
# 1. Get OpenAI API key from https://platform.openai.com/api-keys
# 2. Add to .env:
OPENAI_API_KEY=sk-your-actual-key-here
# 3. Set TEST_MODE=false for production
```

### Issue 7: Messages not showing in console

**Solution:**
- **Verify `TEST_MODE=true` in .env**
- **Check Terminal 1 (backend)** - not Terminal 2 (dashboard)
- **Restart the backend** after changing .env
- **Try triggering an action** (send follow-up, create task, etc.)

### Issue 8: Streamlit shows errors

**Solution:**
```bash
# Clear Streamlit cache
streamlit cache clear

# Check Streamlit version
pip show streamlit

# Reinstall if needed
pip install --upgrade streamlit>=1.39.0
```

---

## 🚀 What's Next? Production Deployment

Once you've tested locally and you're ready to deploy:

### 1. Get Real Credentials

**Twilio (WhatsApp, SMS, Voice):**
1. Sign up at [twilio.com](https://www.twilio.com)
2. Get Account SID and Auth Token
3. Setup WhatsApp Business API or use Sandbox
4. Buy a phone number for SMS/Voice

**Email (SMTP):**
- Use Gmail, Outlook, or any SMTP service
- Generate an app password (not your regular password)
- Configure SMTP settings in .env

**OpenAI (AI Features):**
- Sign up at [platform.openai.com](https://platform.openai.com)
- Create API key
- Add to .env
- Monitor usage and costs

### 2. Update Configuration

```bash
# Edit .env for production:
TEST_MODE=false  # Disable test mode
FLASK_ENV=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@host/dbname  # Use PostgreSQL

# Add real credentials
TWILIO_ACCOUNT_SID=ACxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+1234567890

SMTP_HOST=smtp.gmail.com
SMTP_USER=your-real-email@gmail.com
SMTP_PASSWORD=your-app-password

OPENAI_API_KEY=sk-xxxxxxxx
```

### 3. Deployment Options

**Option A: Traditional Server**
```bash
# Use gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Option B: Docker**
```bash
# Build and run with Docker
docker build -t store-opening-ai .
docker run -p 5000:5000 --env-file .env store-opening-ai
```

**Option C: Cloud Platforms**
- **Heroku:** Easy deployment, PostgreSQL included
- **AWS:** EC2 + RDS, full control
- **Google Cloud:** App Engine, managed service
- **DigitalOcean:** Simple VPS setup

### 4. Setup Monitoring

- **Error Tracking:** Sentry, Rollbar
- **Uptime Monitoring:** UptimeRobot, Pingdom
- **Log Management:** Papertrail, Loggly
- **Performance:** New Relic, Datadog

### 5. Security Checklist

- [ ] Change default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set up firewall rules
- [ ] Regular database backups
- [ ] Monitor API usage
- [ ] Keep dependencies updated
- [ ] Implement rate limiting

---

## 📚 Additional Resources

### Documentation
- **[README.md](./README.md)** - Complete project overview
- **[WORKFLOW_AUTOMATION.md](./docs/WORKFLOW_AUTOMATION.md)** - Workflow details
- **[API_DOCUMENTATION.md](./docs/API_DOCUMENTATION.md)** - API reference
- **[PROCESS_AUTOMATION_CAPABILITIES.md](./PROCESS_AUTOMATION_CAPABILITIES.md)** - Automation features
- **[ML_ADMINLTE_GUIDE.md](./ML_ADMINLTE_GUIDE.md)** - ML features guide

### Quick Guides
- **[QUICKSTART_V2.md](./QUICKSTART_V2.md)** - V2.0 features
- **[AUTOMATION_QUICK_START.md](./AUTOMATION_QUICK_START.md)** - Automation setup
- **[TEST_MODE_GUIDE.md](./TEST_MODE_GUIDE.md)** - Test mode details
- **[QUICKSTART_TWILIO.md](./QUICKSTART_TWILIO.md)** - Twilio setup

### Video Guides (Coming Soon)
- Installing and running locally
- Testing AI communication
- Dashboard walkthrough
- Production deployment

---

## 💬 Get Help

### Common Questions

**Q: Do I need OpenAI API to test locally?**  
A: No! In TEST_MODE, the system uses intelligent default messages and mock predictions.

**Q: Can I use this without Twilio?**  
A: Yes! TEST_MODE allows full functionality without any external services.

**Q: How much does it cost to run in production?**  
A: Depends on usage:
- Twilio: ~$0.005 per WhatsApp message, ~$0.01 per SMS
- OpenAI: ~$0.002 per 1K tokens (GPT-3.5)
- Server: $5-50/month depending on traffic

**Q: Is this production-ready?**  
A: Yes! It's been tested with multiple stores and includes enterprise features.

**Q: Can I customize the AI messages?**  
A: Absolutely! Edit the prompts in `backend/services/ai_service.py`

### Support Channels

- **GitHub Issues:** Report bugs or request features
- **Documentation:** Check the docs folder
- **Code Comments:** Inline explanations in source

---

## 🎉 Conclusion

You now know how to:
✅ Install and run the system locally  
✅ Test AI communication in TEST_MODE  
✅ Understand console output  
✅ Use the API endpoints  
✅ Explore the dashboard features  
✅ Troubleshoot common issues  
✅ Prepare for production deployment  

**Ready to explore?** Start the application and navigate through the dashboard to see all features in action!

---

**Built with ❤️ for efficient store opening management**

*Last Updated: 2024*
