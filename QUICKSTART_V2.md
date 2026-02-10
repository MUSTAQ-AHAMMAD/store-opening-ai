# Store Opening AI - Quick Start Guide

## 🎯 Overview

The **Store Opening AI Management System** is now enhanced with:
- 🔐 **Secure Authentication** - JWT-based login system
- 🎨 **Modern Rich UI** - Professional gradient dashboard
- 🤖 **AI Features** - Intelligent follow-ups and predictions
- 📞 **Voice Calling** - Automated escalations via phone
- 📊 **Advanced Analytics** - Real-time insights and risk assessment

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database & Users
```bash
# Initialize database
python -c "from app import app, db; 
with app.app_context(): db.create_all()"

# Create default users
python data/seed_users.py

# (Optional) Add sample data
python data/seed_beta_data.py
```

### Step 3: Run the Application
```bash
# Terminal 1: Start Backend API
python app.py

# Terminal 2: Start Enhanced Dashboard
streamlit run frontend/dashboard_enhanced.py
```

**Access the app:**
- Backend API: http://localhost:5000
- Dashboard: http://localhost:8501

---

## 🔑 Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Manager | `manager` | `manager123` |
| Team Member | `user` | `user123` |

---

## 🎨 New UI Features

### 1. **Modern Login Page**
- Clean, centered design
- Gradient purple theme
- Registration form
- Password security

### 2. **Rich Dashboard**
- **Gradient Metric Cards**: Beautiful animated cards showing key metrics
- **Color-coded Status**: Visual indicators for all statuses
- **Interactive Charts**: Plotly visualizations with hover effects
- **AI Insights Panel**: Real-time risk assessment and recommendations

### 3. **User Profile**
- Display user name and role
- Quick logout button
- Session management

### 4. **Navigation Sidebar**
- 🏠 Dashboard - Overview and metrics
- 🏪 Stores - Store management
- 👥 Team Members - Team directory
- ✅ Tasks & Checklists - Task tracking
- 💬 WhatsApp - Group messaging
- 📊 Analytics - Reports and charts
- 🤖 AI Insights - Predictions and analysis
- 📞 Voice Escalations - Call management

---

## 🤖 AI Features

### Intelligent Follow-ups
Generates personalized messages based on:
- Task priority and status
- Days overdue
- Store opening timeline
- Team member role

**Example API Call:**
```bash
curl -X POST http://localhost:5000/api/ai/task/1/generate-followup \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Risk Assessment
Analyzes tasks to predict completion likelihood:
```bash
curl http://localhost:5000/api/ai/task/1/risk-assessment \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Completion Prediction
Predicts when a store will be ready:
```bash
curl http://localhost:5000/api/ai/predict/completion-date/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📞 Voice Calling System

### Automatic Escalations
- **Level 0** (0-2 days overdue): WhatsApp reminder
- **Level 1** (3-6 days overdue): Voice call to team member
- **Level 2** (7+ days overdue): Voice call to manager

### Manual Escalation
```bash
curl -X POST http://localhost:5000/api/voice/escalate/task/123 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"escalation_level": 1}'
```

### Voice Call Flow
1. **System initiates call** via Twilio
2. **AI-generated script** plays
3. **Interactive menu** for acknowledgment
4. **System logs** response
5. **Follow-up actions** triggered

---

## 🎨 UI Color Scheme

### Gradient Themes
- **Primary**: Purple (#667eea → #764ba2)
- **Success**: Green (#43e97b → #38f9d7)
- **Warning**: Pink/Red (#f093fb → #f5576c)
- **Info**: Blue (#4facfe → #00f2fe)

### Status Colors
- **Planning**: Gold gradient
- **In Progress**: Blue gradient
- **Completed**: Green gradient
- **Delayed**: Red gradient

---

## 🔧 Configuration

### Required Environment Variables

```bash
# Authentication
SECRET_KEY=your-super-secret-key-change-this

# Twilio (for voice calling)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# OpenAI (for AI features)
OPENAI_API_KEY=sk-your-api-key

# Database
DATABASE_URL=sqlite:///store_opening.db
```

### Optional Features
```bash
# Disable AI features (will use defaults)
# OPENAI_API_KEY=

# Disable scheduler
ENABLE_SCHEDULER=false
```

---

## 📊 API Endpoints

### Authentication
```
POST   /api/auth/register       - Register new user
POST   /api/auth/login          - Login
GET    /api/auth/verify         - Verify token
POST   /api/auth/change-password - Change password
```

### AI Features
```
GET    /api/ai/insights/dashboard          - Dashboard insights
GET    /api/ai/task/<id>/risk-assessment   - Risk analysis
POST   /api/ai/task/<id>/generate-followup - AI message
GET    /api/ai/predict/completion-date/<id> - Predict completion
```

### Voice Calling
```
POST   /api/voice/escalate/task/<id>     - Escalate task
POST   /api/voice/escalate/manager/<id>  - Escalate to manager
GET    /api/voice/call-status/<call_sid> - Check call status
```

---

## 🎯 Key Features Summary

### ✅ Completed Features
- [x] User authentication with JWT
- [x] Role-based access control
- [x] Modern gradient UI design
- [x] Animated metric cards
- [x] AI-powered follow-ups
- [x] Task risk assessment
- [x] Completion prediction
- [x] Voice calling for escalations
- [x] Multi-level escalation system
- [x] Interactive dashboards
- [x] Real-time insights
- [x] Secure password hashing

### 🎨 UI Enhancements
- Professional gradient themes
- Smooth animations and transitions
- Hover effects on cards
- Responsive design
- Status badges with colors
- Interactive charts
- Clean login page
- User profile display

### 🤖 AI Capabilities
- Context-aware message generation
- Historical data analysis
- Risk prediction
- Task prioritization
- Smart recommendations
- Deadline forecasting

### 📞 Voice Features
- Automated calling
- AI-generated scripts
- Interactive menus
- Call logging
- Manager escalations
- SMS fallback

---

## 🔒 Security Features

1. **Password Security**
   - Bcrypt hashing
   - Salt generation
   - Strong password policies

2. **JWT Authentication**
   - Secure token generation
   - 7-day expiration
   - Protected endpoints

3. **Role-Based Access**
   - Admin: Full access
   - Manager: Store management
   - Team Member: Task updates

4. **API Protection**
   - Authorization headers required
   - Token verification
   - Session management

---

## 📱 Dashboard Screenshots

### Login Page
```
┌─────────────────────────────────┐
│     🏪 Store Opening AI         │
│                                 │
│   ┌─────────────────────┐      │
│   │   Welcome Back!     │      │
│   │                     │      │
│   │  Username: [____]   │      │
│   │  Password: [____]   │      │
│   │                     │      │
│   │  [Login] [Register] │      │
│   └─────────────────────┘      │
└─────────────────────────────────┘
```

### Dashboard Overview
```
┌────────────────────────────────────────────┐
│  👤 Admin                    [🚪 Logout]   │
├────────────────────────────────────────────┤
│  🏠 Dashboard Overview                     │
│                                            │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │
│  │  5   │ │ 120  │ │ 75%  │ │  8   │    │
│  │Stores│ │Tasks │ │Done  │ │Alert │    │
│  └──────┘ └──────┘ └──────┘ └──────┘    │
│                                            │
│  🤖 AI-Powered Insights                   │
│  ┌────────────────────────────────────┐  │
│  │ 🔴 Central Plaza - HIGH RISK       │  │
│  │    • 7 days to opening, 60% done   │  │
│  │    ✓ Escalate overdue tasks now    │  │
│  └────────────────────────────────────┘  │
│                                            │
│  📊 Store Progress                        │
│  [Interactive Bar Chart]                  │
└────────────────────────────────────────────┘
```

---

## 🧪 Testing

### Test Authentication
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Get token from response, then:
TOKEN="your-jwt-token"

# Verify
curl http://localhost:5000/api/auth/verify \
  -H "Authorization: Bearer $TOKEN"
```

### Test AI Features
```bash
# Get insights
curl http://localhost:5000/api/ai/insights/dashboard \
  -H "Authorization: Bearer $TOKEN"

# Generate follow-up
curl -X POST http://localhost:5000/api/ai/task/1/generate-followup \
  -H "Authorization: Bearer $TOKEN"
```

### Test Voice Calling
```bash
# Test call (requires Twilio setup)
curl -X POST http://localhost:5000/api/voice/test-call \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"phone":"+1234567890","name":"Test User"}'
```

---

## 🚀 Production Deployment

1. **Update Environment Variables**
   ```bash
   SECRET_KEY=<generate-strong-random-key>
   DATABASE_URL=postgresql://user:pass@host/db
   DEBUG=false
   FLASK_ENV=production
   ```

2. **Use PostgreSQL**
   ```bash
   pip install psycopg2-binary
   # Update DATABASE_URL
   ```

3. **Enable HTTPS**
   - Use reverse proxy (nginx)
   - SSL certificate

4. **Configure Twilio Webhooks**
   - Set production URLs
   - Update webhook endpoints

---

## 📚 Additional Resources

- **Full Documentation**: See `ENHANCED_FEATURES.md`
- **API Reference**: Check endpoint comments in route files
- **Database Models**: See `backend/models/models.py`
- **AI Service**: See `backend/services/ai_service.py`
- **Voice Service**: See `backend/services/voice_service.py`

---

## 🎓 Tips & Tricks

1. **Customize UI Colors**: Edit CSS in `dashboard_enhanced.py`
2. **Adjust AI Behavior**: Modify prompts in `ai_service.py`
3. **Change Voice Scripts**: Edit `voice_service.py`
4. **Add New Roles**: Update User model and auth routes
5. **Extend API**: Add routes in `backend/routes/`

---

## ⚠️ Important Notes

- **Change default passwords** immediately in production
- **Keep API keys secure** - never commit to git
- **Test voice calling** with Twilio sandbox first
- **Monitor AI costs** - OpenAI API has usage fees
- **Enable backups** for production database
- **Use HTTPS** in production environments

---

## 🎉 What's New in V2.0

### Major Improvements
1. ✨ **Professional UI** - Complete redesign with gradients
2. 🔐 **Security** - Full authentication system
3. 🤖 **Intelligence** - AI-powered features
4. 📞 **Voice** - Automated calling system
5. 📊 **Insights** - Advanced analytics

### User Experience
- Faster navigation
- Better visualizations
- Responsive design
- Real-time updates
- Interactive charts

### Business Value
- Reduced manual work
- Faster issue resolution
- Better decision making
- Improved communication
- Higher success rates

---

**Built with ❤️ for efficient store opening management**

For support, check the documentation or review the codebase.
