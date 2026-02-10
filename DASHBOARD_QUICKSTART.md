# Store Opening AI Dashboard - Quick Start Guide

## 🚀 Running the Application

### 1. Start the Backend Server
```bash
cd /home/runner/work/store-opening-ai/store-opening-ai
python app.py
```
The backend will start on `http://localhost:5000`

### 2. Start the Dashboard (in a new terminal)
```bash
cd /home/runner/work/store-opening-ai/store-opening-ai
streamlit run frontend/dashboard_enhanced.py
```
The dashboard will open in your browser at `http://localhost:8501`

## 🔐 First Time Setup

### Create an Account
1. Click the **Register** button on the login page
2. Fill in:
   - Username (required)
   - Email (required)
   - Password (required)
   - Full Name (optional)
3. Click **Create Account**
4. Login with your new credentials

### Login
- Use your username and password
- Session persists until you logout

## 📱 Dashboard Features

### 🏠 Dashboard
- **Overview metrics**: Total stores, tasks, completion rate, overdue tasks
- **AI-powered insights**: Risk analysis and recommendations
- **Store progress charts**: Visual progress tracking
- **Real-time updates**: Latest data from backend

### 🏪 Stores Page
**View Stores:**
- See all stores in expandable cards
- Search by name or location
- Filter by status (planning, in_progress, completed, delayed)
- View completion percentage and progress

**Add New Store:**
1. Click the "Add New Store" tab
2. Fill in store details:
   - Name (required)
   - Location (required)
   - Size in sq ft (required)
   - Manager name
   - Status
   - Opening date
3. Click **Create Store**

**Edit Store:**
1. Click **Edit** button on any store
2. Modify fields in the form
3. Click **Save Changes** or **Cancel**

**Delete Store:**
- Click **Delete** button (confirmation required)

### 👥 Team Members Page
**View Team:**
- Search by name, email, or phone
- Filter by assigned store
- See role and contact information

**Add Team Member:**
1. Expand "Add New Team Member" section
2. Fill in:
   - Name (required)
   - Email (required)
   - Phone (required)
   - Role (team_member/manager/admin)
   - Assign to store
3. Click **Add Member**

**Edit/Delete:**
- Use action buttons on each member card

### ✅ Tasks & Checklists Page
**View Tasks:**
1. Select a store from dropdown
2. Filter by status (pending, in_progress, completed, blocked)
3. View tasks organized by checklist

**Update Task Status:**
- Use the status dropdown on each task
- Changes save automatically

**Task Information:**
- Priority level (🔴 critical, 🟠 high, 🟡 medium, 🟢 low)
- Due date with countdown
- Overdue indicators
- Task description

**Create Checklist:**
1. If no checklists exist, expand "Create New Checklist"
2. Enter checklist name and category
3. Click **Create Checklist**

### 💬 WhatsApp Page
**Groups Tab:**
- View all WhatsApp groups by store
- See recent messages (last 5)
- Check active/inactive status

**Create Group:**
1. Expand "Create New WhatsApp Group"
2. Select store
3. Enter group name and WhatsApp Group ID
4. Click **Create Group**

**Send Message Tab:**
1. Select a group
2. Choose message type:
   - Custom Message: Type your own
   - Task Follow-up: Automated templates
3. Click **Send Message**

### 📊 Analytics Page
**Overall Analytics (All Stores):**
- Total stores and tasks
- Overall completion rate
- Store comparison charts
- Status distribution

**Individual Store Analytics:**
1. Select a specific store from dropdown
2. View:
   - Overall progress percentage
   - Progress by category (bar chart)
   - Task status distribution (pie chart)
   - Progress timeline (line graph)

### 🤖 AI Insights Page
**Select a store to view:**
1. **Completion Prediction**:
   - Predicted completion date
   - On-track status
   - Performance metrics

2. **Task Prioritization**:
   - AI-ranked tasks by priority
   - Top 5 critical tasks

3. **Risk Assessment**:
   - Historical data analysis
   - Risk predictions

### 📞 Voice Escalations Page
- View how automated voice calls work
- Manual escalation triggers (for overdue tasks)
- Escalation levels explained

## 🎨 UI Features

### Professional Sidebar
- **User profile card**: Avatar, name, and role badge
- **Navigation menu**: 8 main sections with icons
- **Hover effects**: Smooth transitions and highlighting
- **Active state**: Visual indicator for current page
- **Logout button**: At bottom of sidebar

### Theme
- **Primary colors**: Purple gradient (#667eea to #764ba2)
- **Status badges**: Color-coded by status
- **Cards**: Modern design with shadows
- **Animations**: Smooth transitions

## 🔧 Troubleshooting

### Backend Not Running
**Error**: "Connection Error: Unable to reach the server"
**Solution**: Start the backend with `python app.py`

### Session Expired
**Error**: "Your session has expired"
**Solution**: Simply login again

### No Data Showing
**Issue**: Empty lists or "No data found"
**Solution**: 
- Ensure backend is running
- Check if data exists in database
- Try refreshing the page (Ctrl+R or Cmd+R)

### API Errors
**Issue**: Error messages when submitting forms
**Solution**:
- Check all required fields are filled
- Ensure valid data formats (dates, numbers)
- Check backend logs for details

## 🧪 Testing the Dashboard

### Test Data Creation
If you need sample data, the backend may have seed scripts:
```bash
python data/seed_saudi_data.py
```

### Manual Testing Steps
1. ✅ Create a store
2. ✅ Add team members
3. ✅ Create checklists and tasks
4. ✅ Update task statuses
5. ✅ View analytics
6. ✅ Check AI insights
7. ✅ Send WhatsApp messages

## 📊 Status Indicators

### Store Status
- **Planning** 🟡: Initial planning phase
- **In Progress** 🔵: Active work ongoing
- **Completed** 🟢: Store opened
- **Delayed** 🔴: Behind schedule

### Task Status
- **Pending** ⏳: Not started
- **In Progress** 🔄: Currently being worked on
- **Completed** ✅: Finished
- **Blocked** ��: Cannot proceed

### Priority Levels
- **Critical** 🔴: Highest priority
- **High** 🟠: Important
- **Medium** 🟡: Normal
- **Low** 🟢: Low priority

## 🔒 Security Notes

- All API calls require authentication
- Sessions expire for security
- Passwords are hashed in backend
- No sensitive data in URLs
- HTTPS recommended for production

## 💡 Tips & Best Practices

1. **Regular Updates**: Update task statuses daily
2. **Use Filters**: Narrow down data with search/filters
3. **Check AI Insights**: Review recommendations regularly
4. **Monitor Analytics**: Track progress trends
5. **Team Coordination**: Use WhatsApp for quick updates
6. **Priority Management**: Focus on critical/high priority tasks

## 📈 Performance

- Dashboard loads in < 2 seconds
- API calls are optimized
- Charts render smoothly with Plotly
- Session state minimizes reloads

## 🆘 Support

For issues or questions:
1. Check this guide
2. Review DASHBOARD_ENHANCEMENT_SUMMARY.md
3. Check backend logs
4. Verify API endpoints are working

## 🎯 Next Steps

After setup:
1. Create your stores
2. Invite team members
3. Set up checklists
4. Assign tasks
5. Monitor progress
6. Use AI insights for optimization

---

**Happy Managing! 🎉**

The Store Opening AI Dashboard makes it easy to manage multiple store openings with powerful features, beautiful UI, and AI-powered insights.
