# Quick Start - New React Frontend

## 🚀 Getting Started with the New React UI

The Store Opening AI system now has a **completely redesigned React.js frontend** with a modern, beautiful interface!

### Prerequisites

Before you start, make sure you have:
- **Node.js 14+** and npm installed
- **Python 3.8+** installed
- **pip** for Python package management

### Step 1: Install Backend Dependencies

```bash
cd /path/to/store-opening-ai
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

```bash
python main.py
```

You should see:
```
==================================================
Store Opening AI - Backend Server
==================================================
Server running on: http://localhost:5000
```

Keep this terminal open.

### Step 3: Install Frontend Dependencies

Open a **new terminal** window:

```bash
cd /path/to/store-opening-ai/react-frontend
npm install
```

This will install all React dependencies (Material-UI, React Router, Axios, etc.)

### Step 4: Start the React Development Server

```bash
npm start
```

After compilation, your browser should automatically open to `http://localhost:3000`

If it doesn't, manually navigate to: **http://localhost:3000**

### Step 5: Login

Use these default credentials:

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Manager Account:**
- Username: `manager`
- Password: `manager123`

**User Account:**
- Username: `user`
- Password: `user123`

## 🎨 What You'll See

### Login Page
- Beautiful purple gradient background
- Tabbed interface for Sign In / Sign Up
- Password visibility toggle
- Modern card-based design

### Dashboard
- **KPI Cards**: Total Stores, Completion Rate, Active Tasks, Overdue Tasks
- **Charts**: Store distribution by status
- **Risk Assessment**: Visual risk level indicators
- **Quick Actions**: Shortcuts to common tasks

### Store Management
- **Grid Layout**: Beautiful cards for each store
- **Search**: Find stores by name or location
- **Filter**: Filter by status (Planning, In Progress, Completed, Delayed)
- **CRUD Operations**: Add, Edit, Delete stores
- **Progress Tracking**: Visual progress bars

## 🔧 Configuration

If you need to change the API URL:

1. Navigate to `react-frontend/`
2. Create or edit `.env` file:
   ```env
   REACT_APP_API_URL=http://localhost:5000/api
   ```
3. Restart the React server

## 📱 Navigation

The sidebar contains:
- 📊 **Dashboard** - Overview and metrics
- 🏪 **Stores** - Manage store openings
- 👥 **Team** - Team management (coming soon)
- ✅ **Tasks** - Task tracking (coming soon)
- 📈 **Analytics** - Detailed analytics (coming soon)
- 🧠 **AI Insights** - AI predictions (coming soon)
- 💬 **WhatsApp** - WhatsApp integration (coming soon)

## 🎯 Key Features

### Authentication
- Secure JWT-based login
- Automatic logout on token expiration
- Protected routes

### Responsive Design
- Works on desktop (>960px)
- Works on tablets (600px-960px)
- Works on mobile (<600px)

### Modern UI
- Purple gradient theme
- Smooth animations
- Hover effects
- Loading states
- Error handling

## 🐛 Troubleshooting

### Backend Connection Issues

**Error**: "Failed to load resource: net::ERR_CONNECTION_REFUSED"

**Solution**:
1. Make sure the backend server is running on port 5000
2. Check that you see "Server running on: http://localhost:5000" in the backend terminal
3. Try accessing http://localhost:5000 in your browser - you should see a JSON response

### React Build Issues

**Error**: "Module not found" or dependency issues

**Solution**:
```bash
cd react-frontend
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use

**Error**: "Port 3000 is already in use"

**Solution**:
```bash
# On Mac/Linux
lsof -ti:3000 | xargs kill -9

# On Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

Or use a different port:
```bash
PORT=3001 npm start
```

## 📚 Further Reading

For complete documentation, see:
- [REACT_FRONTEND_GUIDE.md](./REACT_FRONTEND_GUIDE.md) - Complete React documentation
- [README.md](./README.md) - Main project documentation

## 🎉 Enjoy!

You now have a modern, beautiful React frontend for the Store Opening AI system!

The old Streamlit interface has been completely replaced with this new design.

---

**Need Help?**
- Check the documentation files
- Look at the code comments
- The React app follows standard React patterns

**Version 4.0 - React Edition**
Built with ❤️ using React, TypeScript, and Material-UI
