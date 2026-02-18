# Step-by-Step Guide: Run Locally and Test

## 🎯 Goal
Get the Store Opening AI system running on your computer and test how the AI communicates - **in under 10 minutes**.

---

## ✅ Step 1: Check Your Computer Has Python

Open your terminal (Mac/Linux) or Command Prompt (Windows) and type:

```bash
python --version
```

**What you should see:**
```
Python 3.9.x (or higher)
```

**If you don't have Python 3.9+:**
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH" ✅
- Restart your terminal after installation

---

## ✅ Step 2: Download the Project

```bash
git clone https://github.com/MUSTAQ-AHAMMAD/store-opening-ai.git
cd store-opening-ai
```

**What you should see:**
```
Cloning into 'store-opening-ai'...
remote: Enumerating objects...
✓ Done
```

---

## ✅ Step 3: Run the Setup Script

**On Mac/Linux:**
```bash
./setup.sh
```

**On Windows:**
```cmd
setup.bat
```

**What you should see:**
```
============================================================
Store Opening AI - Quick Setup Script
============================================================

Checking Python version...
Found Python 3.12.3
✅ Python version OK

Creating virtual environment...
✅ Virtual environment created

Installing dependencies...
This may take a few minutes...
✅ Dependencies installed

Setting up environment configuration...
✅ .env file created with TEST_MODE enabled

Initializing database with sample data...
✅ Database initialized

============================================================
Setup Complete! Success!
============================================================
```

**⏱️ This step takes 2-5 minutes** (downloading and installing packages)

**If you see errors:** See the Troubleshooting section at the bottom.

---

## ✅ Step 4: Start the Backend Server

Open a **NEW terminal window** (keep it open).

**On Mac/Linux:**
```bash
cd store-opening-ai
./start_backend.sh
```

**On Windows:**
```cmd
cd store-opening-ai
start_backend.bat
```

**What you should see:**
```
============================================================
Starting Store Opening AI Backend...
============================================================

Starting backend on http://localhost:5000
Press Ctrl+C to stop

==================================================
Store Opening AI - Backend Server
==================================================
Server running on: http://localhost:5000
Debug mode: True
Database: sqlite:///store_opening.db
==================================================

 * Running on http://127.0.0.1:5000
```

**✅ SUCCESS!** The backend is now running.

**⚠️ IMPORTANT:** Keep this terminal window open! Don't close it.

---

## ✅ Step 5: Start the Dashboard

Open a **SECOND NEW terminal window**.

**On Mac/Linux:**
```bash
cd store-opening-ai
./start_dashboard.sh
```

**On Windows:**
```cmd
cd store-opening-ai
start_dashboard.bat
```

**What you should see:**
```
============================================================
Starting Store Opening AI Dashboard...
============================================================

Starting dashboard (will open in browser)...
Press Ctrl+C to stop

You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**✅ SUCCESS!** Your browser should automatically open to the dashboard.

**If browser doesn't open automatically:** Go to http://localhost:8501

---

## ✅ Step 6: Login to the Dashboard

You should now see the login page in your browser.

**Login with these credentials:**
- **Username:** `admin`
- **Password:** `admin123`

**What you should see:**
- A login form with username and password fields
- After login: Dashboard with stores, tasks, and metrics
- A yellow banner at the top saying "🧪 TEST MODE" (this is good!)

---

## ✅ Step 7: Test AI Communication

Now let's see the AI in action!

### Method 1: Through the Dashboard (Easiest)

1. **Click "✅ Tasks & Checklists"** in the sidebar
2. **Select a store** from the dropdown (e.g., "Downtown Tech Hub")
3. **Find any task** in the list
4. **Click the "Send Follow-up" button** next to a task
5. **Go back to Terminal 1** (the backend terminal)
6. **Scroll up** and look for the AI-generated message!

**What you should see in Terminal 1:**
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

**✅ CONGRATULATIONS!** You just saw the AI generate a personalized message!

### Method 2: Using API (For Developers)

Open a **THIRD terminal window** and run:

```bash
# Get an authentication token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Copy the token** from the response (the long string after `"token":`).

Then test AI features:

```bash
# Replace YOUR_TOKEN_HERE with the actual token
TOKEN="YOUR_TOKEN_HERE"

# Generate AI follow-up for task 1
curl -X POST http://localhost:5000/api/ai/task/1/generate-followup \
  -H "Authorization: Bearer $TOKEN"

# Get risk assessment
curl http://localhost:5000/api/ai/task/1/risk-assessment \
  -H "Authorization: Bearer $TOKEN"

# Predict completion date
curl http://localhost:5000/api/ai/predict/completion-date/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Check Terminal 1** again to see the AI output!

---

## ✅ Step 8: Explore the Features

Now that everything is running, explore these sections in the dashboard:

### 🏠 Dashboard
- Overview of all stores
- Key metrics (total stores, tasks, completion rate)
- AI-powered insights and risk assessment

### 🏪 Stores
- View all stores
- See their opening dates
- Check workflow progress (7 stages)
- Material tracking status

### 👥 Team Members
- List of all team members
- Their assigned stores
- Contact information
- Task assignments

### ✅ Tasks & Checklists
- Complete task lists for each store
- Different categories: Hardware, Software, Connectivity, Training
- Priority levels: LOW, MEDIUM, HIGH, CRITICAL
- Send AI-powered follow-ups

### 💬 WhatsApp Groups
- Virtual WhatsApp groups for each store
- Send broadcast messages
- View message history
- Archive conversations

### 📊 Analytics
- Store progress charts
- Task completion trends
- Team performance metrics
- Timeline visualizations

### 🤖 ML & AI
- Machine learning predictions
- Risk assessment scores
- Success probability
- Completion time estimates

---

## 🎉 What Just Happened?

You now have a **fully functional AI-powered store opening management system** running on your computer!

**What's Working:**
- ✅ Backend API server
- ✅ Interactive dashboard
- ✅ Database with sample data
- ✅ AI message generation
- ✅ Machine learning predictions
- ✅ Workflow automation
- ✅ 4 background schedulers (monitoring tasks)

**What's NOT Being Sent:**
- ❌ No real WhatsApp messages (TEST_MODE)
- ❌ No real SMS (TEST_MODE)
- ❌ No real voice calls (TEST_MODE)
- ❌ No real emails (TEST_MODE)

Everything is being **logged to the console** instead, so you can see exactly what the AI would send.

---

## 🔍 What to Test Next

### 1. Create a New Store
1. Go to **🏪 Stores**
2. Click "Add New Store"
3. Fill in the details
4. Watch the workflow stages get created automatically!

### 2. Create a Task
1. Go to **✅ Tasks & Checklists**
2. Select a store
3. Add a new task
4. Set it as overdue (past due date)
5. Wait a few minutes and check Terminal 1 - you'll see automatic escalations!

### 3. Test Workflow Stages
1. Go to **🏪 Stores**
2. Click on a store
3. Complete workflow stages in order
4. Watch as each stage triggers notifications in Terminal 1

### 4. Test Material Tracking
1. Select a store in "In Progress" status
2. Go through stages 2-4 (material tracking)
3. See the logistics chain in action

### 5. Explore ML Predictions
1. Go to **🤖 ML & AI**
2. View risk assessments for different tasks
3. See success probability for stores
4. Check completion time predictions

---

## 🛑 How to Stop

When you're done testing:

1. **Stop the Dashboard:** Go to Terminal 2, press `Ctrl+C`
2. **Stop the Backend:** Go to Terminal 1, press `Ctrl+C`

**To start again later:**
```bash
# Terminal 1
./start_backend.sh    # or start_backend.bat

# Terminal 2  
./start_dashboard.sh  # or start_dashboard.bat
```

---

## 🐛 Troubleshooting

### Problem: "Python not found"
**Solution:**
- Install Python 3.9+ from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal

### Problem: "Permission denied: ./setup.sh"
**Solution (Mac/Linux only):**
```bash
chmod +x setup.sh start_backend.sh start_dashboard.sh
./setup.sh
```

### Problem: "'.' is not recognized as an internal or external command" (Windows)
**Solution:**
On Windows, you cannot use the `./` prefix. Use one of these methods instead:

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

**Explanation:** The `./` syntax is Unix/Linux/Mac specific. Windows Command Prompt doesn't recognize it.

### Problem: "Port 5000 already in use"
**Solution:**
```bash
# On Mac/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
# Note the PID, then:
taskkill /PID <PID_NUMBER> /F
```

### Problem: "Module not found" errors
**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Dashboard shows errors
**Solution:**
1. Make sure Backend (Terminal 1) is running first
2. Clear browser cache
3. Try: `streamlit cache clear`
4. Restart both terminals

### Problem: Can't see AI messages in console
**Solution:**
1. Make sure you're looking at **Terminal 1** (backend), not Terminal 2
2. Verify `.env` has `TEST_MODE=true`
3. Trigger an action (send follow-up, create task)
4. Scroll up in Terminal 1 to see the output

### Problem: Database errors
**Solution:**
```bash
# Reinitialize the database
python data/seed_beta_data.py
```

---

## 📚 Want More Details?

- **Quick Reference:** See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for commands
- **Complete Guide:** See [LOCAL_TESTING_GUIDE.md](./LOCAL_TESTING_GUIDE.md) for everything
- **Visual Flowchart:** See [GETTING_STARTED_FLOWCHART.md](./GETTING_STARTED_FLOWCHART.md)
- **Production Setup:** See [README.md](./README.md) for deploying with real services

---

## 🚀 Next Steps

### Option 1: Keep Testing (Recommended)
- Explore all dashboard features
- Test different scenarios
- Create stores, tasks, team members
- Watch the AI generate different messages

### Option 2: Learn More
- Read the [PROCESS_AUTOMATION_CAPABILITIES.md](./PROCESS_AUTOMATION_CAPABILITIES.md)
- Understand the [7-Stage Workflow](./docs/WORKFLOW_AUTOMATION.md)
- Explore [ML Features](./ML_ADMINLTE_GUIDE.md)

### Option 3: Deploy to Production
- Get Twilio account (WhatsApp, SMS, Voice)
- Get OpenAI API key (for AI features)
- Set up email SMTP
- Change `TEST_MODE=false` in `.env`
- Deploy to cloud (Heroku, AWS, etc.)

---

## ❓ Quick Q&A

**Q: Do I need Twilio or OpenAI accounts to test?**
A: NO! TEST_MODE works without any external accounts.

**Q: Will this send real messages?**
A: NO! In TEST_MODE, everything is logged to console only.

**Q: How do I see the AI communication?**
A: Check Terminal 1 (backend) after triggering any action.

**Q: Can I use this in production?**
A: YES! Just configure real credentials and set TEST_MODE=false.

**Q: How much does it cost to run?**
A: Testing is FREE. Production costs depend on Twilio/OpenAI usage.

**Q: Is my data saved?**
A: YES! Everything is saved in the SQLite database (store_opening.db).

**Q: Can I reset everything?**
A: YES! Just run `python data/seed_beta_data.py` again.

---

## ✅ Checklist: Did Everything Work?

- [ ] Python 3.9+ installed and working
- [ ] Project cloned successfully
- [ ] Setup script completed without errors
- [ ] Backend server started (Terminal 1)
- [ ] Dashboard opened in browser (Terminal 2)
- [ ] Logged in with admin/admin123
- [ ] Saw the TEST MODE banner
- [ ] Clicked "Send Follow-up" on a task
- [ ] Saw AI-generated message in Terminal 1
- [ ] Explored dashboard features

**If you checked all boxes: CONGRATULATIONS! 🎉**

You're now ready to explore the full power of the Store Opening AI system!

---

## 💬 Need Help?

- **GitHub Issues:** Report problems or ask questions
- **Documentation:** Check the docs/ folder
- **Console Logs:** Look at Terminal 1 for detailed error messages

---

**Built with ❤️ for efficient store opening management**

*Last Updated: February 2024*
