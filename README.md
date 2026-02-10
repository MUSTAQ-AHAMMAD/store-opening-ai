# Store Opening AI Management System

## 🎉 NEW: Version 3.0 - Complete Workflow Automation!

**Latest Updates:**
- 🔄 **7-Stage Workflow Process** - Automated store opening process management
- 📧 **Email Notifications** - Multi-channel communication (WhatsApp + Email + SMS + Voice)
- 🤖 **AI-Powered Follow-ups** - Intelligent, context-aware messaging
- ⚡ **Automatic Timeline Recalculation** - Dynamic deadline management
- 🔔 **Multi-Level Escalations** - Automatic escalations for delays
- 📦 **Material Tracking** - Track shipments from warehouse to store
- 💻 **TeamViewer Integration** - Remote support during installation
- 🎯 **100% On-Time Store Openings** - Strict follow-ups and process automation

> **Workflow Guide**: See [WORKFLOW_AUTOMATION.md](./docs/WORKFLOW_AUTOMATION.md) for the complete workflow automation guide!

## 🎉 Version 2.0 Features
- 🔐 **User Authentication** - Secure login with JWT
- 🎨 **Modern Rich UI** - Professional gradient dashboard
- 🤖 **AI Features** - Intelligent follow-ups and predictions
- 📞 **Voice Calling** - Automated escalations via phone
- 📊 **Advanced Analytics** - Real-time insights and risk assessment

> **Quick Start**: See [QUICKSTART_V2.md](./QUICKSTART_V2.md) for the new features guide!

---

A comprehensive Python-based AI system for managing store opening logistics with automated WhatsApp follow-ups, real-time tracking, and data archival.

## 🌟 Features

### Core Functionality
- **7-Stage Workflow Process**: Automated process from store creation to opening
- **Store Management**: Create and track multiple store openings with timelines
- **Team Management**: Manage team members across different stores
- **Task Tracking**: Comprehensive checklist system with priority levels
- **WhatsApp Integration**: Automated messaging and group management via Twilio
- **Email Notifications**: Professional HTML emails for all workflow events
- **SMS & Voice Escalations**: Multi-channel escalations for delays
- **Automated Follow-ups**: Scheduled reminders and escalations for overdue tasks
- **Material Tracking**: Track shipments from warehouse → nearby store → actual store
- **TeamViewer Support**: Remote installation support with mandatory ID tracking
- **Analytics Dashboard**: Real-time progress tracking and reporting
- **Data Archival**: Preserve group conversations and historical data

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Frontend**: Streamlit (Interactive dashboard)
- **Database**: SQLite (development) with PostgreSQL migration support
- **WhatsApp**: Twilio WhatsApp Business API
- **Email**: SMTP (Gmail, Outlook, etc.)
- **SMS & Voice**: Twilio API
- **AI**: OpenAI GPT for intelligent messaging
- **Scheduling**: APScheduler for automated tasks
- **Visualization**: Plotly for charts and analytics

## 📋 Prerequisites

- Python 3.9 or higher (Python 3.12+ recommended for best compatibility)
- pip (Python package manager)
- Twilio account (for WhatsApp, SMS, and Voice integration)
- Email account with SMTP access (for email notifications)
- OpenAI API key (optional, for AI-powered messages)

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/MUSTAQ-AHAMMAD/store-opening-ai.git
cd store-opening-ai
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
# Upgrade pip, setuptools, and wheel to ensure compatibility with pre-built wheels
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///store_opening.db

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+1234567890

# Email Configuration (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com

# OpenAI Configuration (optional, for AI-powered messages)
OPENAI_API_KEY=your_openai_api_key_here

# Scheduler Configuration
SCHEDULER_TIMEZONE=UTC
ENABLE_SCHEDULER=true
```

## 📊 7-Stage Workflow Process

The system implements a comprehensive workflow automation:

1. **Stage 1 - Update Nearby Store Details** (20 days before opening)
   - Team member provides nearby store information
   - Contact person and mobile number required

2. **Stage 2 - Complete Checklist & Send to Warehouse** (18 days before)
   - Team completes all checklist items
   - Material requirements sent to warehouse

3. **Stage 3 - Confirm Material at Nearby Store** (15 days before)
   - Same team member confirms material arrival at nearby store

4. **Stage 4 - Confirm Material at Actual Store** (12 days before)
   - Material transported and confirmed at actual store location

5. **Stage 5 - Start Installation & TeamViewer ID** (1 day before or on opening day)
   - Installation process begins
   - **TeamViewer ID mandatory** for remote support

6. **Stage 6 - Final Checklist** (Opening day)
   - Complete final verification checklist
   - Ensure all systems operational

7. **Stage 7 - Store Opening Complete** (Opening day)
   - Store opening marked as complete
   - Success notification sent to all

### Automatic Features:
- 📧 Email notifications for each stage
- 💬 WhatsApp group updates in real-time
- ⏰ Automatic deadline calculations
- 🔄 Timeline recalculation when opening date changes
- 🚨 Multi-level escalations for delays (WhatsApp → SMS → Call → Email)
- 🤖 AI-generated follow-up messages

> See [WORKFLOW_AUTOMATION.md](./docs/WORKFLOW_AUTOMATION.md) for complete workflow documentation

## 🗄️ Database Setup

### Initialize the database and seed beta testing data
```bash
python data/seed_beta_data.py
```

This will create:
- **Default user accounts** for login (admin, manager, user)
- 5 sample stores with different opening dates
- **Workflow stages** for each store
- 20+ team members across stores
- Complete checklists for each store (Hardware, Software, Connectivity, Training)
- Sample tasks with various statuses and priorities
- WhatsApp groups for each store
- Mock conversation data for archived groups
- Follow-up reminders and escalations

### Default Login Credentials
After seeding, you can login with these credentials:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Manager | `manager` | `manager123` |
| Team Member | `user` | `user123` |

> ⚠️ **Security Note**: Change these default passwords in production!

## 🏃 Running the Application

### Start the Backend API Server
```bash
python main.py
# or alternatively:
python app.py
```

The API server will start on `http://localhost:5000`

### Start the Dashboard (in a separate terminal)
```bash
streamlit run frontend/dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📱 WhatsApp Integration Setup

### 1. Create a Twilio Account
- Sign up at [twilio.com](https://www.twilio.com)
- Navigate to the WhatsApp section
- Get your Account SID and Auth Token

### 2. Configure WhatsApp Sandbox (Development)
- In Twilio Console, go to Messaging > Try it out > WhatsApp
- Follow the instructions to join the sandbox
- Use the sandbox number as your `TWILIO_WHATSAPP_NUMBER`

### 3. Production Setup
- Apply for WhatsApp Business API access
- Get your business number approved
- Update the configuration with your production number

## 🎯 Usage Guide

### Dashboard Navigation

1. **🏠 Dashboard**
   - Overview of all stores and tasks
   - Key metrics and statistics
   - Upcoming store openings
   - Progress visualization

2. **🏪 Stores**
   - View all stores
   - Create new store openings
   - Track store details and progress
   - Update store status

3. **👥 Team Members**
   - Manage team members
   - Filter by store
   - View team statistics
   - Assign tasks

4. **✅ Checklists & Tasks**
   - View all checklists by store
   - Track task completion
   - Update task status
   - Monitor due dates and priorities

5. **💬 WhatsApp Groups**
   - Manage group communications
   - Send messages to team
   - View archived conversations
   - Track message history

6. **📊 Analytics**
   - Dashboard overview
   - Store progress reports
   - Task analysis
   - Completion trends

### API Endpoints

#### Stores
- `GET /api/stores` - List all stores
- `GET /api/stores/<id>` - Get store details
- `POST /api/stores` - Create new store
- `PUT /api/stores/<id>` - Update store
- `DELETE /api/stores/<id>` - Delete store
- `GET /api/stores/<id>/summary` - Get comprehensive summary

#### Team Members
- `GET /api/team` - List all team members
- `GET /api/team/<id>` - Get team member details
- `POST /api/team` - Create team member
- `PUT /api/team/<id>` - Update team member
- `DELETE /api/team/<id>` - Delete team member

#### Checklists & Tasks
- `GET /api/checklists` - List all checklists
- `POST /api/checklists` - Create checklist
- `GET /api/checklists/<id>/tasks` - Get tasks for checklist
- `POST /api/checklists/<id>/tasks` - Create task
- `PUT /api/checklists/tasks/<id>` - Update task
- `DELETE /api/checklists/tasks/<id>` - Delete task

#### WhatsApp
- `GET /api/whatsapp/groups` - List WhatsApp groups
- `POST /api/whatsapp/groups` - Create group
- `POST /api/whatsapp/groups/<id>/send` - Send message
- `POST /api/whatsapp/groups/<id>/archive` - Archive group
- `GET /api/whatsapp/groups/<id>/archive` - Get archived conversations

#### Workflow (NEW!)
- `GET /api/workflow/store/<id>/stages` - Get all workflow stages
- `GET /api/workflow/store/<id>/stages/<num>` - Get specific stage
- `POST /api/workflow/store/<id>/nearby-store` - Update nearby store details (Stage 1)
- `GET /api/workflow/store/<id>/nearby-store` - Get nearby store details
- `POST /api/workflow/store/<id>/warehouse-shipment` - Confirm warehouse shipment (Stage 2)
- `POST /api/workflow/store/<id>/nearby-store-receipt` - Confirm nearby store receipt (Stage 3)
- `POST /api/workflow/store/<id>/store-receipt` - Confirm store receipt (Stage 4)
- `POST /api/workflow/store/<id>/installation` - Start installation with TeamViewer (Stage 5)
- `GET /api/workflow/store/<id>/installation` - Get installation details
- `PUT /api/workflow/store/<id>/installation` - Update installation notes
- `POST /api/workflow/store/<id>/final-checklist` - Complete final checklist (Stage 6)
- `POST /api/workflow/store/<id>/complete` - Mark store opening complete (Stage 7)
- `GET /api/workflow/store/<id>/material-tracking` - Get material tracking status
- `PUT /api/workflow/store/<id>/opening-date` - Update opening date (recalculates timelines)
- `GET /api/workflow/store/<id>/escalations` - Get escalation history
- `GET /api/workflow/store/<id>/delayed-stages` - Get delayed stages

#### Analytics
- `GET /api/analytics/dashboard` - Dashboard analytics
- `GET /api/analytics/store/<id>/progress` - Store progress
- `GET /api/analytics/report` - Generate report

## 🤖 Automated Follow-up System

The system includes an automated scheduler that:

1. **Hourly Follow-ups**: Checks for pending follow-up messages and sends them
2. **Overdue Task Monitoring**: Every 6 hours, checks for overdue tasks and sends escalations
3. **Daily Summaries**: Sends daily progress summaries to team members at 9 AM

### Escalation Levels
- **Level 0**: Normal reminder (task approaching due date)
- **Level 1**: First escalation (3+ days overdue)
- **Level 2**: Critical escalation (7+ days overdue)

## 📊 Beta Testing Data

The seed script creates realistic testing data:

### Stores
1. Downtown Tech Hub (New York) - Opening in 15 days - In Progress
2. Westside Electronics (Los Angeles) - Opening in 30 days - Planning
3. Central Plaza Store (Chicago) - Opening in 7 days - In Progress
4. Bay Area Outlet (San Francisco) - Opening in 45 days - Planning
5. Metro Center (Boston) - Opened 5 days ago - Completed

### Checklists per Store
- Hardware Setup (POS, Printers, Scanners, Cameras, Network)
- Software & Accounts (Employee accounts, Inventory software, POS config)
- Connectivity (Internet, SIM cards, WiFi, Payment gateway)
- Training & Documentation (Staff training, Manuals, Security protocols)

## 🔧 Development

### Project Structure
```
store-opening-ai/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── backend/
│   ├── models/
│   │   └── models.py          # Database models
│   ├── routes/
│   │   ├── store_routes.py    # Store API endpoints
│   │   ├── team_routes.py     # Team member endpoints
│   │   ├── checklist_routes.py # Checklist/task endpoints
│   │   ├── whatsapp_routes.py # WhatsApp endpoints
│   │   └── analytics_routes.py # Analytics endpoints
│   └── services/
│       ├── whatsapp_service.py # WhatsApp integration
│       └── scheduler.py        # Automated follow-up scheduler
├── frontend/
│   └── dashboard.py           # Streamlit dashboard
├── data/
│   └── seed_beta_data.py      # Beta testing data seed script
└── README.md                  # This file
```

### Running Tests
```bash
pytest
```

### Database Migrations

For production, migrate to PostgreSQL:
```bash
# Update .env
DATABASE_URL=postgresql://user:password@localhost/store_opening

# Run migration (implement with Flask-Migrate if needed)
```

## 📚 Documentation

- [API Documentation](./docs/API_DOCUMENTATION.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Typing Best Practices](./docs/TYPING_BEST_PRACTICES.md) - **Important for Python 3.13+ compatibility**

## 🐛 Troubleshooting

### Common Issues

1. **Database not found**
   ```bash
   python data/seed_beta_data.py
   ```

2. **API connection error in dashboard**
   - Ensure Flask app is running on port 5000
   - Check firewall settings

3. **WhatsApp messages not sending**
   - Verify Twilio credentials in `.env`
   - Check account balance
   - Confirm phone numbers are in correct format

4. **Scheduler not running**
   - Check `ENABLE_SCHEDULER=true` in `.env`
   - Review logs for errors

5. **Dependency installation fails on Windows**
   - **Solution**: Ensure pip, setuptools, and wheel are up to date:
     ```bash
     pip install --upgrade pip setuptools wheel
     pip install -r requirements.txt
     ```
   - The requirements.txt now uses numpy >=2.1.0 which has pre-built wheels for Python 3.9+, including Python 3.12+
   - **Note**: NumPy 2.x requires Python 3.9 or higher. If you're using Python 3.8, you'll need to use numpy 1.x (not compatible with this project's current configuration)
   - **Recommended**: Use Python 3.9 or higher (Python 3.12+ recommended for best compatibility)
   - If you still encounter build errors, ensure your Python version is 3.9 or higher

6. **`can't open file 'main.py'` error**
   - Both `python main.py` and `python app.py` are valid entry points
   - Make sure you are in the `store-opening-ai` project directory before running the command

7. **NamedTuple or typing errors**
   - See [Typing Best Practices](./docs/TYPING_BEST_PRACTICES.md) for correct NamedTuple syntax
   - Common issue: Using dict syntax `{'field': type}` instead of list syntax `[('field', type)]`
   - **Python 3.13+ compatibility**: Always use class-based `NamedTuple` syntax (recommended)

## 📝 License

This project is for educational and internal use.

## 🤝 Contributing

Contributions are welcome! Please create an issue or pull request.

## 📧 Support

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ for efficient store opening management**