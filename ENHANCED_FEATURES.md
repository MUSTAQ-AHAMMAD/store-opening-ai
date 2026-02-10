# Enhanced Store Opening AI - Version 2.0

## 🎉 What's New

This major update transforms the Store Opening AI system with a **professional dashboard UI**, **user authentication**, **AI-powered features**, and **voice calling for escalations**.

## 🚀 New Features

### 1. **User Authentication & Management**
- Secure login system with JWT tokens
- Role-based access control (Admin, Manager, Team Member)
- Password hashing with bcrypt
- Session management
- User registration and profile management

### 2. **Modern, Rich Dashboard UI**
- Completely redesigned interface with gradient themes
- Professional card-based layout
- Animated transitions and hover effects
- Responsive design for all screen sizes
- Dark/light color schemes
- Interactive charts and visualizations

### 3. **Advanced AI Features**
- **Intelligent Follow-ups**: AI-generated personalized messages
- **Task Prioritization**: Smart recommendations for task ordering
- **Risk Assessment**: Predict task completion likelihood
- **Completion Predictions**: Estimate project completion dates
- **AI Insights**: Automated recommendations and alerts

### 4. **Voice Calling for Escalations**
- Automated voice calls for overdue tasks
- Multi-level escalation system:
  - **Level 0**: WhatsApp reminder (0-2 days overdue)
  - **Level 1**: Voice call to team member (3-6 days overdue)
  - **Level 2**: Voice call to manager (7+ days overdue)
- Interactive voice menus for acknowledgment
- Call logging and status tracking
- Fallback SMS when calls fail

### 5. **Enhanced Security**
- Password hashing and salting
- JWT-based authentication
- Protected API endpoints
- Role-based permissions
- Session timeout management

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- Twilio account (for WhatsApp and Voice)
- OpenAI API key (for AI features)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here

# Twilio Configuration (Required for voice calls)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# OpenAI Configuration (Required for AI features)
OPENAI_API_KEY=sk-your-openai-api-key

# Database
DATABASE_URL=sqlite:///store_opening.db

# Scheduler
ENABLE_SCHEDULER=true
```

### 3. Initialize Database
```bash
# Create database tables
python app.py

# Seed with sample data
python data/seed_beta_data.py

# Create default users
python data/seed_users.py
```

### 4. Run the Application

**Backend API:**
```bash
python app.py
```
Server runs on `http://localhost:5000`

**Enhanced Dashboard:**
```bash
streamlit run frontend/dashboard_enhanced.py
```
Dashboard opens at `http://localhost:8501`

## 🔐 Default Login Credentials

After running `seed_users.py`, use these credentials:

| Role | Username | Password | Email |
|------|----------|----------|-------|
| Admin | `admin` | `admin123` | admin@storeai.com |
| Manager | `manager` | `manager123` | manager@storeai.com |
| Team Member | `user` | `user123` | user@storeai.com |

**⚠️ IMPORTANT:** Change these passwords immediately in production!

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify` - Verify JWT token
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/users` - List users (admin only)
- `POST /api/auth/change-password` - Change password

### AI Analytics
- `GET /api/ai/task/<id>/risk-assessment` - Get task risk analysis
- `GET /api/ai/store/<id>/task-prioritization` - Get AI task priorities
- `POST /api/ai/task/<id>/generate-followup` - Generate AI follow-up message
- `GET /api/ai/insights/dashboard` - Get AI-powered insights
- `GET /api/ai/predict/completion-date/<store_id>` - Predict completion date

### Voice Calling
- `POST /api/voice/escalate/task/<id>` - Make voice escalation call
- `POST /api/voice/escalate/manager/<id>` - Escalate to manager
- `POST /api/voice/acknowledgment` - Handle call acknowledgment (webhook)
- `POST /api/voice/manager-acknowledgment` - Handle manager acknowledgment
- `GET /api/voice/call-status/<call_sid>` - Get call status
- `POST /api/voice/test-call` - Test voice calling

## 🤖 AI Features Details

### Intelligent Follow-ups
The AI service generates context-aware messages considering:
- Days overdue
- Task priority
- Store opening timeline
- Overall project progress
- Team member role

Example:
```python
# Get AI-generated follow-up
response = requests.post(
    'http://localhost:5000/api/ai/task/1/generate-followup',
    headers={'Authorization': f'Bearer {token}'}
)
```

### Task Prioritization
AI analyzes all pending tasks and suggests optimal ordering based on:
- Time sensitivity
- Dependencies
- Critical path
- Current status
- Days until opening

### Risk Assessment
Predicts completion likelihood by analyzing:
- Historical task completion data
- Similar task patterns
- Current progress velocity
- Team performance trends

## 📞 Voice Calling System

### How It Works
1. **Automated Monitoring**: Scheduler checks for overdue tasks every 6 hours
2. **Escalation Levels**:
   - 0-2 days: WhatsApp reminder with AI message
   - 3-6 days: Voice call to assigned team member
   - 7+ days: Voice call to manager + WhatsApp to team

### Voice Call Flow
1. System initiates call via Twilio
2. Recipient answers
3. AI-generated message plays
4. Options presented:
   - Press 1 to acknowledge
   - Press 2 for support
5. System logs response
6. Follow-up action taken

### Manual Escalation
Managers can manually trigger voice calls:
```python
response = requests.post(
    'http://localhost:5000/api/voice/escalate/task/123',
    json={'escalation_level': 2},
    headers={'Authorization': f'Bearer {token}'}
)
```

## 🎨 UI Features

### Dashboard Components
- **Metric Cards**: Animated gradient cards with key metrics
- **AI Insights Panel**: Real-time risk assessments and recommendations
- **Progress Charts**: Interactive Plotly visualizations
- **Task Management**: Checkbox-based task completion
- **Responsive Layout**: Works on desktop, tablet, and mobile

### Color Scheme
- Primary: Purple gradient (#667eea to #764ba2)
- Success: Green gradient (#43e97b to #38f9d7)
- Warning: Orange gradient (#f093fb to #f5576c)
- Info: Blue gradient (#4facfe to #00f2fe)

### Animations
- Fade-in effects on page load
- Hover transformations on cards
- Smooth transitions on all interactions
- Loading spinners for async operations

## 🔒 Security Best Practices

1. **Always change default passwords**
2. **Use strong SECRET_KEY in production**
3. **Enable HTTPS in production**
4. **Rotate JWT tokens regularly**
5. **Keep API keys secure**
6. **Use environment variables for sensitive data**
7. **Implement rate limiting on login endpoints**
8. **Enable database backups**

## 🧪 Testing

### Test Authentication
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Verify token
curl -X GET http://localhost:5000/api/auth/verify \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Voice Calling
```bash
curl -X POST http://localhost:5000/api/voice/test-call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"phone":"+1234567890","name":"Test User"}'
```

### Test AI Features
```bash
# Get AI insights
curl -X GET http://localhost:5000/api/ai/insights/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"

# Generate follow-up
curl -X POST http://localhost:5000/api/ai/task/1/generate-followup \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📊 Architecture

### Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: Streamlit with custom CSS
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Authentication**: JWT (PyJWT)
- **AI**: OpenAI GPT-3.5/4
- **Voice**: Twilio Voice API
- **Messaging**: Twilio WhatsApp API
- **Scheduling**: APScheduler
- **Visualization**: Plotly

### System Flow
```
User → Enhanced Dashboard (Streamlit)
         ↓
      Flask API (with JWT auth)
         ↓
    ┌────┴────┬──────────┬──────────┐
    ↓         ↓          ↓          ↓
Database   AI Service  Voice     WhatsApp
(SQLite)   (OpenAI)    Service   Service
                       (Twilio)  (Twilio)
```

## 🚀 Production Deployment

### 1. Update Configuration
```bash
# .env for production
SECRET_KEY=<generate-strong-random-key>
DATABASE_URL=postgresql://user:pass@host/db
DEBUG=false
FLASK_ENV=production
```

### 2. Database Migration
```bash
# Migrate to PostgreSQL
pip install psycopg2-binary
# Update DATABASE_URL in .env
python app.py  # Creates tables
```

### 3. Deploy Options
- **Heroku**: Use Procfile
- **AWS**: EC2 + RDS
- **Google Cloud**: App Engine
- **Docker**: Use Dockerfile

### 4. Configure Twilio Webhooks
Point Twilio webhooks to your production URLs:
- Voice acknowledgment: `https://yourdomain.com/api/voice/acknowledgment`
- Manager acknowledgment: `https://yourdomain.com/api/voice/manager-acknowledgment`

## 📝 Changelog

### Version 2.0.0 (Current)
- ✅ User authentication and authorization
- ✅ Modern, rich dashboard UI
- ✅ AI-powered intelligent follow-ups
- ✅ Task prioritization with AI
- ✅ Risk assessment and predictions
- ✅ Voice calling for escalations
- ✅ Multi-level escalation system
- ✅ Enhanced security features
- ✅ Responsive design
- ✅ Animated UI components

### Version 1.0.0 (Previous)
- Basic dashboard
- Store management
- Task tracking
- WhatsApp integration
- Scheduled follow-ups

## 🤝 Contributing

Contributions are welcome! Please ensure:
1. Code follows existing style
2. Tests pass
3. Documentation is updated
4. Security best practices followed

## 📄 License

This project is for internal use. All rights reserved.

## 📧 Support

For issues or questions:
1. Check documentation
2. Review API endpoints
3. Test with curl/Postman
4. Check logs for errors

## 🎯 Roadmap

### Planned Features
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Custom report builder
- [ ] Email notifications
- [ ] SMS notifications (non-WhatsApp)
- [ ] Calendar integration
- [ ] Document management
- [ ] Real-time collaboration
- [ ] Video conferencing integration

---

**Built with ❤️ for efficient store opening management**
