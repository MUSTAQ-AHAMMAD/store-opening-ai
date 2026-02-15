# Process Automation - Troubleshooting Guide

## Common Issues and Solutions

This guide helps you resolve common issues with the automation system.

---

## 🔍 Scheduler Issues

### Issue: Scheduler Not Running

**Symptoms:**
- No automated follow-ups being sent
- Workflow delays not being detected
- Daily summaries not sent

**Solution:**

1. Check if scheduler is enabled in `.env`:
```bash
ENABLE_SCHEDULER=true
```

2. Check console logs for scheduler startup message:
```
Follow-up scheduler started
```

3. Restart the application:
```bash
python main.py
```

4. Verify jobs are configured:
```python
# Check scheduler.py has all 4 jobs:
- check_follow_ups (hourly)
- check_overdue_tasks (every 6 hours)
- check_workflow_delays (every 2 hours)
- send_daily_summary (daily at 9 AM)
```

---

### Issue: Jobs Running But No Actions Taken

**Symptoms:**
- Scheduler logs show jobs running
- But no escalations or notifications

**Solution:**

1. Check for overdue tasks in database:
```bash
# Using Python console
from backend.models.models import Task
from datetime import datetime

overdue = Task.query.filter(
    Task.due_date < datetime.utcnow(),
    Task.status != 'completed'
).all()

print(f"Overdue tasks: {len(overdue)}")
```

2. Check for delayed workflow stages:
```bash
curl http://localhost:5000/api/workflow/store/1/delayed-stages
```

3. Verify follow-ups exist:
```python
from backend.models.models import FollowUp
pending = FollowUp.query.filter_by(status='pending').count()
print(f"Pending follow-ups: {pending}")
```

---

## 📱 Notification Issues

### Issue: Messages Not Sending (Test Mode)

**Symptoms:**
- No console output showing messages
- Notifications appear to be silent

**Solution:**

This is expected! In test mode, messages are logged to console:

```bash
# Check console for output like:
============================================================
📱 WhatsApp Message (Test Mode)
============================================================
```

If you don't see this:
1. Verify `TEST_MODE=true` in `.env`
2. Check console output (not just logs)
3. Restart application to reload environment

---

### Issue: Messages Not Sending (Production Mode)

**Symptoms:**
- TEST_MODE=false
- No messages being received
- No errors in logs

**Solution:**

**For WhatsApp (Twilio):**

1. Verify Twilio credentials:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

2. Check Twilio account status:
   - Login to twilio.com
   - Check account balance
   - Verify WhatsApp sandbox is active (for development)

3. Verify phone numbers are in E.164 format:
```
✅ Correct: +12345678900
❌ Wrong: (123) 456-7890
❌ Wrong: 123-456-7890
```

4. Check Twilio logs for delivery status:
   - Go to Twilio Console > Monitor > Logs
   - Look for failed messages

**For Email (SMTP):**

1. Verify email configuration:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password  # NOT your regular password!
FROM_EMAIL=your_email@gmail.com
```

2. For Gmail, create App Password:
   - Go to Google Account > Security
   - Enable 2-factor authentication
   - Generate App Password
   - Use this as SMTP_PASSWORD

3. Test email manually:
```bash
curl -X POST http://localhost:5000/api/test/email \
  -H "Content-Type: application/json" \
  -d '{"to": "test@example.com", "subject": "Test", "body": "Test email"}'
```

**For Voice Calls:**

1. Verify Twilio phone number is configured:
```bash
TWILIO_PHONE_NUMBER=+12345678900  # Must be a verified Twilio number
```

2. Check phone number is verified in Twilio:
   - Go to Twilio Console > Phone Numbers
   - Verify number is active and has voice capability

3. Test voice call manually:
```bash
curl -X POST http://localhost:5000/api/voice/test-call \
  -H "Content-Type: application/json" \
  -d '{"phone": "+12345678900", "name": "Test User"}'
```

---

## 🔄 Workflow Issues

### Issue: Workflow Stages Not Advancing

**Symptoms:**
- Stage completed but next stage not starting
- Workflow stuck on one stage

**Solution:**

1. Check if previous stage is completed:
```bash
curl http://localhost:5000/api/workflow/store/1/stages
```

Look for:
```json
{
  "stage_number": 1,
  "status": "completed",  // Must be "completed"
  "completed_at": "2024-01-15T10:30:00Z"
}
```

2. Verify required fields are provided:
```bash
# Stage 1 requires:
- nearby_store_name
- nearby_store_address
- contact_person_name
- contact_person_mobile
- updated_by_id

# Stage 5 requires:
- teamviewer_id (MANDATORY)
- technician_id
```

3. Check for database errors in logs:
```bash
# Look for SQLAlchemy errors like:
# - IntegrityError
# - NOT NULL constraint failed
```

4. Verify team member IDs exist:
```bash
curl http://localhost:5000/api/team/1
```

---

### Issue: Timeline Not Recalculating

**Symptoms:**
- Opening date changed
- Stage due dates didn't update

**Solution:**

1. Use the correct endpoint:
```bash
# ✅ Correct:
PUT /api/workflow/store/{id}/opening-date
{
  "opening_date": "2024-06-01T00:00:00Z"
}

# ❌ Wrong:
PUT /api/stores/{id}
{
  "opening_date": "2024-06-01"
}
```

2. Check only incomplete stages are updated:
   - Completed stages keep original dates
   - Only pending/in_progress stages recalculate

3. Verify date format:
```
✅ Correct: "2024-06-01T00:00:00Z"
❌ Wrong: "2024-06-01"
❌ Wrong: "06/01/2024"
```

---

## 🤖 AI & ML Issues

### Issue: AI Messages Not Generating

**Symptoms:**
- Generic messages instead of AI-generated
- "AI not available" errors

**Solution:**

1. Check OpenAI API key:
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

2. Verify API key is valid:
   - Login to platform.openai.com
   - Check API keys section
   - Ensure key has credits

3. Check for API errors in logs:
```
OpenAI API Error: Invalid API key
OpenAI API Error: Rate limit exceeded
OpenAI API Error: Insufficient quota
```

4. System uses fallback messages when AI unavailable:
```python
# If you see generic messages like:
"Please complete the task: [Task Name]"

# AI service is not working, check logs
```

---

### Issue: ML Models Not Predicting

**Symptoms:**
- Risk assessment returns "insufficient data"
- Predictions show "N/A"
- Model statistics show 0 samples

**Solution:**

1. ML models need minimum 10 samples to train:
```bash
curl http://localhost:5000/api/ml/stats

# Check response:
{
  "completion_predictor": {
    "samples": 3,  // Need at least 10
    "trained": false
  }
}
```

2. Train models from completed stores:
```bash
# Train from single store
curl -X POST http://localhost:5000/api/ml/learn/store/5

# Batch train from multiple stores
curl -X POST http://localhost:5000/api/ml/learn/batch \
  -H "Content-Type: application/json" \
  -d '{"store_ids": [1, 2, 3, 4, 5]}'
```

3. Only completed stores can be used for training:
```python
# Store must have:
- status = "completed"
- opening_date in the past
- tasks exist with completion data
```

4. Check model files exist:
```bash
ls -la data/ml_models/
# Should see:
# - completion_predictor.pkl
# - risk_assessor.pkl
# - task_duration.pkl
# - success_factors.pkl
```

---

## 📦 Material Tracking Issues

### Issue: Material Status Not Updating

**Symptoms:**
- Material tracking shows "pending"
- Status doesn't change after stage completion

**Solution:**

1. Material tracking starts at Stage 2:
```bash
# Stage 1: No material tracking yet
# Stage 2: warehouse_shipped_at set, status = "shipped"
# Stage 3: nearby_store_received_at set, status = "at_nearby_store"
# Stage 4: store_received_at set, status = "delivered"
```

2. Complete stages in order:
```bash
POST /api/workflow/store/1/nearby-store      # Stage 1
POST /api/workflow/store/1/warehouse-shipment # Stage 2 (starts tracking)
POST /api/workflow/store/1/nearby-store-receipt # Stage 3
POST /api/workflow/store/1/store-receipt      # Stage 4
```

3. Check material tracking:
```bash
curl http://localhost:5000/api/workflow/store/1/material-tracking

# Response shows:
{
  "status": "delivered",
  "warehouse_shipped_at": "2024-01-05T10:00:00Z",
  "nearby_store_received_at": "2024-01-08T14:30:00Z",
  "store_received_at": "2024-01-12T09:15:00Z"
}
```

---

## 🔐 Authentication Issues

### Issue: API Returns 401 Unauthorized

**Symptoms:**
- Dashboard can't connect to API
- API returns "Unauthorized" errors

**Solution:**

1. Most endpoints don't require authentication:
```bash
# These work without auth:
GET /api/stores
GET /api/team
GET /api/workflow/store/{id}/stages
```

2. If authentication is required:
```bash
# Login first
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Use token in subsequent requests
curl http://localhost:5000/api/protected-endpoint \
  -H "Authorization: Bearer YOUR_TOKEN"
```

3. Check default users exist:
```bash
# Seed users if needed
python data/seed_users.py
```

---

## 🗄️ Database Issues

### Issue: Database Tables Don't Exist

**Symptoms:**
- "no such table" errors
- "relation does not exist" errors

**Solution:**

1. Initialize database:
```bash
python data/seed_beta_data.py
```

2. Or manually:
```python
from app import app, db
with app.app_context():
    db.create_all()
```

3. Check database file exists:
```bash
ls -la store_opening.db
```

---

### Issue: Database Locked

**Symptoms:**
- "database is locked" errors
- Writes fail intermittently

**Solution:**

1. Close other connections:
   - Stop any other processes accessing the database
   - Close any database browser tools

2. Use PostgreSQL for production:
```bash
# Update .env
DATABASE_URL=postgresql://user:password@localhost/store_opening
```

3. Increase timeout (SQLite only):
```python
# In app.py
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'timeout': 30}
}
```

---

## 🧪 Testing Issues

### Issue: Tests Failing

**Symptoms:**
- pytest shows failures
- Import errors

**Solution:**

1. Install test dependencies:
```bash
pip install pytest pytest-flask
```

2. Set test mode:
```bash
export TEST_MODE=true
export ENABLE_SCHEDULER=false
```

3. Run specific test:
```bash
python -m pytest test_automation_capabilities.py::test_all_services_loaded -v
```

4. Check for common issues:
   - Database schema changes
   - API signature changes
   - Missing fixtures

---

## 📊 Performance Issues

### Issue: Slow API Responses

**Symptoms:**
- API takes >5 seconds to respond
- Dashboard is sluggish

**Solution:**

1. Check database query performance:
```python
# Enable SQL logging
app.config['SQLALCHEMY_ECHO'] = True
```

2. Add database indexes:
```python
# For frequently queried fields
class Store(db.Model):
    __tablename__ = 'stores'
    
    # Add indexes
    __table_args__ = (
        db.Index('idx_store_status', 'status'),
        db.Index('idx_store_opening_date', 'opening_date'),
    )
```

3. Use pagination:
```bash
# Don't fetch all records at once
GET /api/stores?page=1&per_page=20
```

4. Optimize ML predictions:
   - Cache predictions for 1 hour
   - Use batch predictions
   - Limit training dataset size

---

### Issue: High Memory Usage

**Symptoms:**
- Process using >1GB RAM
- System slows down over time

**Solution:**

1. Limit ML model memory:
```python
# In ml_learning_service.py
self.max_training_samples = 1000  # Limit dataset size
```

2. Clear old escalation history:
```python
# Keep only last 90 days
from datetime import datetime, timedelta
from backend.models.models import EscalationHistory

cutoff = datetime.utcnow() - timedelta(days=90)
EscalationHistory.query.filter(
    EscalationHistory.created_at < cutoff
).delete()
db.session.commit()
```

3. Use production WSGI server:
```bash
# Instead of Flask development server:
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🔧 Configuration Issues

### Issue: Environment Variables Not Loading

**Symptoms:**
- Default values used instead of .env
- Configuration seems to be ignored

**Solution:**

1. Check .env file exists:
```bash
ls -la .env
```

2. Verify python-dotenv is installed:
```bash
pip install python-dotenv
```

3. Check .env is loaded:
```python
# In app.py, ensure this is at the top:
from dotenv import load_dotenv
load_dotenv()
```

4. Restart application after .env changes:
```bash
# Stop and restart
python main.py
```

5. Check for syntax errors in .env:
```bash
# ✅ Correct:
TEST_MODE=true
ENABLE_SCHEDULER=false

# ❌ Wrong:
TEST_MODE = true  # No spaces around =
ENABLE_SCHEDULER: false  # Use =, not :
```

---

## 🆘 Getting Help

If issues persist after trying these solutions:

1. **Check Logs:**
```bash
# Console output shows detailed errors
# Look for stack traces
```

2. **Enable Debug Mode:**
```bash
DEBUG=true
FLASK_ENV=development
```

3. **Review Documentation:**
- [PROCESS_AUTOMATION_CAPABILITIES.md](./PROCESS_AUTOMATION_CAPABILITIES.md)
- [WORKFLOW_AUTOMATION.md](./docs/WORKFLOW_AUTOMATION.md)
- [API_DOCUMENTATION.md](./docs/API_DOCUMENTATION.md)

4. **Test Individual Components:**
```python
# Test services independently
from backend.services.whatsapp_service import WhatsAppService
ws = WhatsAppService()
# Try sending test message
```

5. **Create GitHub Issue:**
   - Include error messages
   - Provide steps to reproduce
   - Share relevant configuration (without secrets)

---

## ✅ Prevention Checklist

To avoid common issues:

- [ ] Always use test mode first before production
- [ ] Verify all environment variables are set
- [ ] Run database seeds after schema changes
- [ ] Check Twilio account balance regularly
- [ ] Monitor ML model training samples
- [ ] Keep dependencies updated
- [ ] Use production database (PostgreSQL) for scale
- [ ] Set up proper logging and monitoring
- [ ] Regular backups of database
- [ ] Test automation in staging environment

---

**Need more help?** Create an issue on GitHub with details about your problem.

**Built with ❤️ for reliable process automation**
