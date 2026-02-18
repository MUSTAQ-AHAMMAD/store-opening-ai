# 🚀 Quick Reference Card

## One-Page Setup Guide

### Prerequisites
```bash
✓ Python 3.9+ (check: python --version)
✓ Git installed
✓ Terminal/Command Prompt
```

### Setup (5 Minutes)
```bash
# 1. Clone & Navigate
git clone https://github.com/MUSTAQ-AHAMMAD/store-opening-ai.git
cd store-opening-ai

# 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4. Configure Test Mode
cp .env.example .env
# Edit .env: Set TEST_MODE=true

# 5. Initialize Database
python data/seed_beta_data.py

# 6. Start Backend (Terminal 1)
python main.py

# 7. Start React Dashboard (Terminal 2)
./start_dashboard.sh  # or start_dashboard.bat on Windows
```

### Access
- **Backend API:** http://localhost:5000
- **React Dashboard:** http://localhost:3000
- **Login:** admin / admin123

---

## Test AI Communication

### Through Dashboard
1. Login → **✅ Tasks & Checklists**
2. Select a store
3. Click **"Send Follow-up"** on any task
4. **Check Terminal 1** for AI message output

### Through API
```bash
# 1. Get Auth Token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. Test AI Follow-up
TOKEN="your_token_here"
curl -X POST http://localhost:5000/api/ai/task/1/generate-followup \
  -H "Authorization: Bearer $TOKEN"

# 3. Test Risk Assessment
curl http://localhost:5000/api/ai/task/1/risk-assessment \
  -H "Authorization: Bearer $TOKEN"

# 4. Test Completion Prediction
curl http://localhost:5000/api/ai/predict/completion-date/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Console Output (What to Look For)

### WhatsApp Message Example
```
============================================================
📱 WhatsApp Message (Test Mode)
============================================================
To: whatsapp:+1234567890
Store: Downtown Tech Hub
Task: Install POS System

Message:
🔔 Task Reminder - Action Required
...
============================================================
```

### Voice Call Example
```
============================================================
📞 Voice Call (Test Mode)
============================================================
To: John Doe (+1234567890)
Task: Install POS System
Days Overdue: 3
Escalation Level: 2

Call Script:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hello John Doe, this is the Store Opening AI System.
This is an URGENT escalation...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
============================================================
```

---

## Key Features to Test

### 1. Workflow Automation (7 Stages)
```bash
# Get workflow stages
curl http://localhost:5000/api/workflow/store/1/stages \
  -H "Authorization: Bearer $TOKEN"

# Complete Stage 1
curl -X POST http://localhost:5000/api/workflow/store/1/nearby-store \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nearby_store_name":"Warehouse #5","contact_person":"Jane","contact_mobile":"+1234567890"}'
```

### 2. Material Tracking
```bash
# Track material through logistics
curl http://localhost:5000/api/workflow/store/1/material-tracking \
  -H "Authorization: Bearer $TOKEN"
```

### 3. ML Predictions
```bash
# Get store success probability
curl http://localhost:5000/api/ml/store/1/success-probability \
  -H "Authorization: Bearer $TOKEN"

# Get task completion prediction
curl http://localhost:5000/api/ml/task/1/completion-prediction \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Multi-Level Escalations
```bash
# Manual escalation (Level 1)
curl -X POST http://localhost:5000/api/voice/escalate/task/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"escalation_level": 1}'
```

---

## Dashboard Navigation

| Section | What You'll Find |
|---------|------------------|
| 🏠 **Dashboard** | Overview, metrics, AI insights |
| 🏪 **Stores** | Create/manage stores, workflow status |
| 👥 **Team Members** | Team directory, assignments |
| ✅ **Tasks & Checklists** | Task tracking, send follow-ups |
| 💬 **WhatsApp Groups** | Group management, broadcasting |
| 📊 **Analytics** | Charts, reports, trends |
| 🤖 **ML & AI** | Risk assessment, predictions |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Database not found | `python data/seed_beta_data.py` |
| Port 5000 in use | Kill process or change PORT in .env |
| Dashboard won't open | Check backend is running first |
| Messages not showing | Verify TEST_MODE=true, check Terminal 1 |

---

## Background Schedulers (Automatic)

When backend runs, these schedulers activate:

1. **Hourly** - Sends pending follow-up messages
2. **2-Hour** - Monitors workflow stage delays
3. **6-Hour** - Detects overdue tasks, triggers escalations
4. **Daily (9 AM)** - Sends progress summaries

**Watch Terminal 1 to see automated actions!**

---

## Default Login Accounts

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| manager | manager123 | Manager |
| user | user123 | Team Member |

---

## Escalation Levels

| Level | Trigger | Action |
|-------|---------|--------|
| 0 | Due soon | WhatsApp reminder |
| 1 | 3+ days overdue | WhatsApp escalation |
| 2 | 5+ days overdue | SMS notification |
| 3 | 7+ days overdue | Voice call |
| 4 | Critical | Manager email |

---

## Test Mode vs Production

| Feature | Test Mode | Production |
|---------|-----------|------------|
| AI Messages | ✅ Console | ✅ Real channels |
| Voice Calls | ✅ Script shown | ✅ Actual call |
| Emails | ✅ Logged | ✅ Real email |
| SMS | ✅ Logged | ✅ Real SMS |
| WhatsApp | ✅ Logged | ✅ Real WhatsApp |
| Workflow | ✅ Full | ✅ Full |
| ML Models | ✅ Full | ✅ Full |

---

## Production Checklist

- [ ] Set TEST_MODE=false
- [ ] Add real Twilio credentials
- [ ] Configure SMTP email
- [ ] Add OpenAI API key (optional)
- [ ] Change default passwords
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Setup monitoring
- [ ] Configure backups

---

## Useful Links

- 📖 **[LOCAL_TESTING_GUIDE.md](./LOCAL_TESTING_GUIDE.md)** - Complete testing guide
- 📘 **[README.md](./README.md)** - Full documentation
- 🚀 **[QUICKSTART_V2.md](./QUICKSTART_V2.md)** - V2.0 features
- 🤖 **[PROCESS_AUTOMATION_CAPABILITIES.md](./PROCESS_AUTOMATION_CAPABILITIES.md)** - Automation reference
- 🧠 **[ML_ADMINLTE_GUIDE.md](./ML_ADMINLTE_GUIDE.md)** - ML features
- 🔄 **[WORKFLOW_AUTOMATION.md](./docs/WORKFLOW_AUTOMATION.md)** - Workflow details
- 📚 **[API_DOCUMENTATION.md](./docs/API_DOCUMENTATION.md)** - API reference

---

## Quick Commands

```bash
# Restart Backend
Ctrl+C in Terminal 1, then: python main.py

# Restart React Dashboard
Ctrl+C in Terminal 2, then: ./start_dashboard.sh  # or start_dashboard.bat

# Clear React build cache
cd react-frontend
rm -rf build node_modules/.cache
cd ..

# Check Logs
tail -f backend.log  # if logging to file

# Reinitialize Database
python data/seed_beta_data.py
```

---

## Get Help

- **GitHub Issues:** Report bugs/request features
- **Documentation:** Check docs/ folder
- **Code Comments:** Inline explanations
- **Console Output:** Check Terminal 1 for detailed logs

---

**Built with ❤️ for efficient store opening management**

*Print this page for quick reference!*
