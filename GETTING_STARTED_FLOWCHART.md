# 🎯 Getting Started - Visual Flowchart

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│         Store Opening AI - Quick Start Decision Tree               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

                              START HERE
                                  │
                                  │
                    ┌─────────────▼─────────────┐
                    │  What do you want to do?  │
                    └─────────────┬─────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
     ┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐
     │  Test Locally    │  │   Deploy to  │  │  Learn About     │
     │  (No accounts)   │  │  Production  │  │  Features        │
     └────────┬─────────┘  └──────┬───────┘  └────────┬─────────┘
              │                    │                    │
              │                    │                    │
              ▼                    ▼                    ▼


╔══════════════════════════════════════════════════════════════════════╗
║                       OPTION 1: TEST LOCALLY                         ║
╚══════════════════════════════════════════════════════════════════════╝

    Step 1: Clone Repository
    ┌──────────────────────────────────────┐
    │ git clone <repo-url>                 │
    │ cd store-opening-ai                  │
    └──────────────────────────────────────┘
                    │
                    ▼
    Step 2: Automated Setup
    ┌──────────────────────────────────────┐
    │ Linux/Mac:  ./setup.sh               │
    │ Windows:    setup.bat                │
    │                                      │
    │ This automatically:                  │
    │ • Checks Python 3.9+                 │
    │ • Creates virtual environment        │
    │ • Installs dependencies              │
    │ • Sets TEST_MODE=true                │
    │ • Initializes database               │
    └──────────────────────────────────────┘
                    │
                    ▼
    Step 3: Start Application
    ┌──────────────────────────────────────┐
    │ Terminal 1:                          │
    │   ./start_backend.sh                 │
    │   (or start_backend.bat)             │
    │                                      │
    │ Terminal 2:                          │
    │   ./start_dashboard.sh               │
    │   (or start_dashboard.bat)           │
    └──────────────────────────────────────┘
                    │
                    ▼
    Step 4: Test AI Communication
    ┌──────────────────────────────────────┐
    │ 1. Open http://localhost:8501        │
    │ 2. Login: admin / admin123           │
    │ 3. Go to Tasks & Checklists          │
    │ 4. Click "Send Follow-up"            │
    │ 5. Check Terminal 1 for AI output    │
    └──────────────────────────────────────┘
                    │
                    ▼
                SUCCESS! 🎉
    ┌──────────────────────────────────────┐
    │ You're now testing AI communication! │
    │ All messages appear in console.      │
    │                                      │
    │ Next: Explore the dashboard or try  │
    │ API endpoints (see QUICK_REFERENCE)  │
    └──────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════╗
║                    OPTION 2: DEPLOY TO PRODUCTION                    ║
╚══════════════════════════════════════════════════════════════════════╝

    Step 1: Test Locally First
    ┌──────────────────────────────────────┐
    │ Follow "Option 1: Test Locally"      │
    │ Make sure everything works           │
    └──────────────────────────────────────┘
                    │
                    ▼
    Step 2: Get Required Accounts
    ┌──────────────────────────────────────┐
    │ ✓ Twilio Account                     │
    │   • WhatsApp Business API            │
    │   • Phone number for SMS/Voice       │
    │   • Get: Account SID, Auth Token     │
    │                                      │
    │ ✓ Email Account (SMTP)               │
    │   • Gmail/Outlook with app password  │
    │                                      │
    │ ✓ OpenAI API Key (optional)          │
    │   • For AI-powered features          │
    └──────────────────────────────────────┘
                    │
                    ▼
    Step 3: Update Configuration
    ┌──────────────────────────────────────┐
    │ Edit .env:                           │
    │                                      │
    │ TEST_MODE=false                      │
    │ FLASK_ENV=production                 │
    │ DEBUG=false                          │
    │                                      │
    │ Add real credentials:                │
    │ • TWILIO_ACCOUNT_SID=ACxxx...        │
    │ • TWILIO_AUTH_TOKEN=xxx...           │
    │ • SMTP_USER=your@email.com           │
    │ • OPENAI_API_KEY=sk-xxx...           │
    └──────────────────────────────────────┘
                    │
                    ▼
    Step 4: Deploy
    ┌──────────────────────────────────────┐
    │ Choose deployment method:            │
    │                                      │
    │ A) Cloud Platform:                   │
    │    • Heroku                          │
    │    • AWS (EC2 + RDS)                 │
    │    • Google Cloud                    │
    │    • DigitalOcean                    │
    │                                      │
    │ B) Docker:                           │
    │    docker build -t store-ai .        │
    │    docker run -p 5000:5000 store-ai  │
    │                                      │
    │ C) Traditional Server:               │
    │    gunicorn -w 4 -b 0.0.0.0:5000 app │
    └──────────────────────────────────────┘
                    │
                    ▼
    Step 5: Setup Monitoring
    ┌──────────────────────────────────────┐
    │ • Error tracking (Sentry)            │
    │ • Uptime monitoring (UptimeRobot)    │
    │ • Log management (Papertrail)        │
    │ • Performance (New Relic)            │
    └──────────────────────────────────────┘
                    │
                    ▼
              PRODUCTION READY! 🚀


╔══════════════════════════════════════════════════════════════════════╗
║                     OPTION 3: LEARN ABOUT FEATURES                   ║
╚══════════════════════════════════════════════════════════════════════╝

    Documentation to Read:
    ┌──────────────────────────────────────────────────────────────┐
    │                                                              │
    │ 1. README.md                                                 │
    │    └─> Complete project overview                            │
    │                                                              │
    │ 2. LOCAL_TESTING_GUIDE.md                                    │
    │    └─> How to test AI communication locally                 │
    │                                                              │
    │ 3. QUICK_REFERENCE.md                                        │
    │    └─> One-page cheat sheet                                 │
    │                                                              │
    │ 4. PROCESS_AUTOMATION_CAPABILITIES.md                        │
    │    └─> Complete automation features                         │
    │                                                              │
    │ 5. WORKFLOW_AUTOMATION.md                                    │
    │    └─> 7-stage workflow details                             │
    │                                                              │
    │ 6. ML_ADMINLTE_GUIDE.md                                      │
    │    └─> Machine learning features                            │
    │                                                              │
    │ 7. API_DOCUMENTATION.md                                      │
    │    └─> API endpoint reference                               │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘

    Key Features to Explore:
    ┌──────────────────────────────────────────────────────────────┐
    │                                                              │
    │ 🤖 AI Communication                                          │
    │    • Intelligent follow-up messages                         │
    │    • Context-aware escalations                              │
    │    • Risk assessment                                        │
    │    • Completion predictions                                 │
    │                                                              │
    │ 🔄 Workflow Automation (7 Stages)                            │
    │    • Nearby store details                                   │
    │    • Checklist completion                                   │
    │    • Material tracking (4 checkpoints)                      │
    │    • Installation & TeamViewer                              │
    │    • Final verification                                     │
    │    • Store opening complete                                 │
    │                                                              │
    │ 📊 Machine Learning                                          │
    │    • 4 self-learning models                                 │
    │    • 78%+ prediction accuracy                               │
    │    • Historical data analysis                               │
    │    • Success pattern recognition                            │
    │                                                              │
    │ 🚨 Multi-Level Escalations                                   │
    │    • Level 0: WhatsApp reminder                             │
    │    • Level 1: WhatsApp escalation                           │
    │    • Level 2: SMS notification                              │
    │    • Level 3: Voice call                                    │
    │    • Level 4: Manager email                                 │
    │                                                              │
    │ 📱 Multi-Channel Communication                               │
    │    • WhatsApp (via Twilio)                                  │
    │    • SMS                                                    │
    │    • Voice calls                                            │
    │    • Email (HTML templates)                                 │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════

                          QUICK HELP GUIDE

Question: Can I test without Twilio/OpenAI accounts?
Answer:  YES! Use TEST_MODE=true (enabled by default after setup)
         All messages will be logged to console.

Question: How do I see AI communication?
Answer:  1. Start backend with ./start_backend.sh
         2. Trigger an action (send follow-up, create task, etc.)
         3. Check Terminal 1 - you'll see formatted AI messages!

Question: What Python version do I need?
Answer:  Python 3.9 or higher (3.12+ recommended)

Question: Do I need a database?
Answer:  SQLite is included and auto-created. No setup needed!
         For production, you can upgrade to PostgreSQL.

Question: How do I run on Windows?
Answer:  Use .bat files instead of .sh files:
         • setup.bat (instead of ./setup.sh)
         • start_backend.bat
         • start_dashboard.bat

Question: What are the default login credentials?
Answer:  admin / admin123
         manager / manager123
         user / user123

Question: Where can I see console output?
Answer:  Terminal 1 (backend) shows all messages, API calls, and logs
         Terminal 2 (dashboard) shows Streamlit interface logs

Question: How do I troubleshoot issues?
Answer:  See LOCAL_TESTING_GUIDE.md section "Troubleshooting"
         Common fixes:
         • Module not found: pip install -r requirements.txt
         • Port in use: Change PORT in .env or kill process
         • Database error: python data/seed_beta_data.py

═══════════════════════════════════════════════════════════════════════

                         SUPPORT & RESOURCES

📖 Documentation:
   • LOCAL_TESTING_GUIDE.md    - Complete testing guide
   • QUICK_REFERENCE.md        - One-page cheat sheet
   • README.md                 - Full project documentation

🔗 Quick Links:
   • GitHub Issues             - Report bugs
   • API Reference             - docs/API_DOCUMENTATION.md
   • Workflow Guide            - docs/WORKFLOW_AUTOMATION.md

💬 Getting Help:
   1. Check LOCAL_TESTING_GUIDE.md troubleshooting section
   2. Review QUICK_REFERENCE.md for common commands
   3. Check console output in Terminal 1 for error messages
   4. Open GitHub issue with detailed error description

═══════════════════════════════════════════════════════════════════════

                    Built with ❤️ for efficient store opening management
```
