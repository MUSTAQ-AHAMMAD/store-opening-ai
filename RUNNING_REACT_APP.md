# 🚀 Running the Store Opening AI with React.js Frontend

## 📋 Complete Step-by-Step Guide

This guide will walk you through **everything** you need to run the Store Opening AI application with its modern React.js frontend. Perfect for beginners!

---

## ✅ Prerequisites

Before starting, make sure you have these installed on your computer:

### Required Software

1. **Python 3.9 or higher** (Python 3.12+ recommended)
   - Check: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/
   - ⚠️ On Windows: Check "Add Python to PATH" during installation

2. **Node.js 14 or higher** (Node.js 16+ recommended)
   - Check: `node --version`
   - Download: https://nodejs.org/
   - This includes npm (Node Package Manager)

3. **Git** (for cloning the repository)
   - Check: `git --version`
   - Download: https://git-scm.com/

### Optional but Recommended

- **VS Code** or any code editor
- A modern web browser (Chrome, Firefox, Edge, Safari)

---

## 📥 Step 1: Get the Code

### Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/MUSTAQ-AHAMMAD/store-opening-ai.git
cd store-opening-ai

# OR using SSH (if you have SSH keys set up)
git clone git@github.com:MUSTAQ-AHAMMAD/store-opening-ai.git
cd store-opening-ai
```

### Verify You're in the Right Directory

```bash
ls -la
# You should see: README.md, requirements.txt, react-frontend/, backend/, etc.
```

---

## ⚙️ Step 2: Set Up the Backend

The backend is a Flask API that the React frontend communicates with.

### Option A: Automated Setup (Recommended)

**On Mac/Linux:**
```bash
./setup.sh
```

**On Windows:**
```cmd
setup.bat
```

This script will:
- ✅ Create a Python virtual environment
- ✅ Install Python dependencies
- ✅ Install React frontend dependencies
- ✅ Set up the database
- ✅ Configure environment variables

### Option B: Manual Setup

If the automated script doesn't work, follow these manual steps:

#### 2.1 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the beginning of your terminal prompt.

#### 2.2 Install Python Dependencies

```bash
# Upgrade pip first (optional but recommended)
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt
```

This will install Flask, SQLAlchemy, and other backend dependencies.

#### 2.3 Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# On Windows:
copy .env.example .env
```

The default `.env` file will work for local testing.

#### 2.4 Initialize the Database

```bash
# Seed the database with sample data
python data/seed_beta_data.py
```

This creates:
- Sample stores
- Test users (admin, manager, user)
- Demo tasks and checklists

---

## 🎨 Step 3: Set Up the React Frontend

The frontend is a modern React.js application with TypeScript and Material-UI.

### 3.1 Navigate to the Frontend Directory

```bash
cd react-frontend
```

### 3.2 Install Node.js Dependencies

```bash
npm install
```

This will install:
- React and React Router
- TypeScript
- Material-UI components
- Axios (for API calls)
- Recharts (for data visualization)
- And more...

**This may take 2-5 minutes depending on your internet speed.**

### 3.3 Configure Frontend Environment (Optional)

If you need to change the backend API URL:

```bash
# Create .env file in react-frontend directory
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env
```

The default configuration points to `http://localhost:5000/api` which works for local development.

---

## 🚀 Step 4: Start the Application

You need **TWO terminal windows** running simultaneously:
1. Backend API (Flask)
2. Frontend UI (React)

### Terminal 1: Start the Backend

From the **project root directory** (not inside react-frontend):

```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Start the backend server
python main.py

# Alternative:
python app.py
```

**Expected Output:**
```
==================================================
Store Opening AI - Backend Server
==================================================
Server running on: http://localhost:5000
Debug mode: True
Database: sqlite:///store_opening.db
==================================================

 * Running on http://127.0.0.1:5000
```

✅ **Success!** Leave this terminal running.

⚠️ **Troubleshooting:**
- If port 5000 is in use, you'll see an error. Kill the process using that port or change the port in `.env`
- Make sure your virtual environment is activated

### Terminal 2: Start the React Frontend

Open a **NEW terminal window** and navigate to the frontend:

```bash
cd store-opening-ai/react-frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view react-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully
```

✅ **Success!** Your browser should automatically open to http://localhost:3000

⚠️ **Troubleshooting:**
- If port 3000 is in use, you'll be prompted to use a different port (usually 3001). Press 'Y' to continue.
- If the browser doesn't open automatically, manually navigate to http://localhost:3000

---

## 🎯 Step 5: Access and Login

### 5.1 Open Your Browser

Navigate to: **http://localhost:3000**

You should see a beautiful login page with a purple gradient background.

### 5.2 Login with Default Credentials

The system comes with pre-configured test accounts:

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Full access to all features

**Manager Account:**
- Username: `manager`
- Password: `manager123`
- Management-level access

**User Account:**
- Username: `user`
- Password: `user123`
- Standard user access

### 5.3 Explore the Dashboard

After logging in, you'll see:

1. **📊 Dashboard** - Overview with KPIs and charts
   - Total stores
   - Completion rate
   - Active tasks
   - Risk assessment

2. **🏪 Stores** - Manage store openings
   - View all stores in a card grid
   - Search and filter
   - Add new stores
   - Edit/delete existing stores

3. **👥 Team** - Team management (coming soon)

4. **✅ Tasks** - Task tracking (coming soon)

5. **📈 Analytics** - Detailed analytics (coming soon)

6. **🧠 AI Insights** - AI predictions (coming soon)

7. **💬 WhatsApp** - Communication (coming soon)

---

## 🎨 What You Should See

### Login Page Features:
- ✨ Beautiful purple gradient background
- 🔐 Secure login form
- 👁️ Password visibility toggle
- 📝 Sign up option (if registration is enabled)

### Dashboard Features:
- 📊 KPI cards with live metrics
- 📈 Interactive charts
- ⚠️ Risk assessment panel
- 🎯 Quick action buttons
- 🔍 Search functionality

### Store Management:
- 🎴 Card-based grid layout
- 🔍 Real-time search
- 🏷️ Status filtering (Planning, In Progress, Completed, Delayed)
- ➕ Add new store button
- ✏️ Edit/Delete actions
- 📊 Progress indicators

---

## 🛑 How to Stop the Application

### Stop the Frontend
In Terminal 2 (React frontend):
- Press `Ctrl + C`
- Confirm with `Y` if prompted

### Stop the Backend
In Terminal 1 (Flask backend):
- Press `Ctrl + C`

---

## 🔄 Restarting the Application

### Quick Restart (Daily Use)

**Terminal 1 - Backend:**
```bash
cd store-opening-ai
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd store-opening-ai/react-frontend
npm start
```

### After Updates

If you pulled new code or dependencies changed:

**Backend:**
```bash
pip install -r requirements.txt
python data/seed_beta_data.py  # if database schema changed
```

**Frontend:**
```bash
cd react-frontend
npm install
```

---

## 🐛 Troubleshooting

### Problem: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Frontend shows "Connection Refused"

**Error:** `Failed to load resource: net::ERR_CONNECTION_REFUSED`

**Solution:**
1. Make sure the backend is running (Terminal 1 should show "Running on http://127.0.0.1:5000")
2. Check that backend is on port 5000
3. Try accessing http://localhost:5000 in browser - you should see JSON data
4. Check `.env` file in react-frontend directory

### Problem: Port Already in Use

**Error:** `Address already in use` or `Port 5000 is already in use`

**Solution:**

**On Mac/Linux:**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or for port 3000
lsof -ti:3000 | xargs kill -9
```

**On Windows:**
```cmd
# Find process on port 5000
netstat -ano | findstr :5000

# Kill it (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Problem: npm install fails

**Error:** Various npm errors

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Problem: Database errors

**Error:** `no such table` or database errors

**Solution:**
```bash
# Delete the database and recreate it
rm store_opening.db
python data/seed_beta_data.py
```

### Problem: Login doesn't work

**Error:** `401 Unauthorized` or `Invalid credentials`

**Solution:**
1. Make sure you're using correct credentials: `admin` / `admin123`
2. Check backend logs in Terminal 1 for errors
3. Try resetting the database: `python data/seed_beta_data.py`
4. Clear browser localStorage (F12 → Application → Local Storage → Clear)

---

## 🎯 Quick Commands Reference

### Backend Commands
```bash
# Start backend
python main.py

# Reset database
python data/seed_beta_data.py

# Run tests
pytest

# Check database
sqlite3 store_opening.db "SELECT * FROM user;"
```

### Frontend Commands
```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint  # if configured

# Clear cache
rm -rf node_modules package-lock.json && npm install
```

---

## 📦 Production Deployment

When ready to deploy to production:

### Backend
```bash
# Set production environment
export FLASK_ENV=production  # or set in .env

# Use production-grade server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```bash
# Build optimized production bundle
cd react-frontend
npm run build

# Serve the build folder with a static server
# Options: nginx, Apache, serve, etc.
npx serve -s build -l 3000
```

### Environment Variables

Update your `.env` files:
- Set `DEBUG=False`
- Set `SECRET_KEY` to a secure random string
- Configure production database (PostgreSQL recommended)
- Set proper CORS origins
- Enable HTTPS

---

## 🔒 Security Notes

### For Local Development:
- ✅ Default credentials are fine for testing
- ✅ SQLite database is sufficient
- ✅ TEST_MODE can be enabled

### For Production:
- ⚠️ Change all default passwords
- ⚠️ Use PostgreSQL or MySQL instead of SQLite
- ⚠️ Enable HTTPS
- ⚠️ Configure proper CORS settings
- ⚠️ Set strong SECRET_KEY
- ⚠️ Disable TEST_MODE
- ⚠️ Set up proper logging and monitoring

---

## 📚 Additional Resources

### Documentation Files
- **[REACT_QUICKSTART.md](./REACT_QUICKSTART.md)** - Quick start guide
- **[REACT_FRONTEND_GUIDE.md](./REACT_FRONTEND_GUIDE.md)** - Complete frontend documentation
- **[README.md](./README.md)** - Main project documentation
- **[LOCAL_TESTING_GUIDE.md](./LOCAL_TESTING_GUIDE.md)** - Testing guide
- **[FRONTEND_MIGRATION.md](./FRONTEND_MIGRATION.md)** - Migration from Streamlit

### Need Help?
- Check the troubleshooting section above
- Review the documentation files
- Check the code comments
- The React app follows standard React patterns

---

## ✅ Success Checklist

- [ ] Python 3.9+ installed and accessible
- [ ] Node.js 14+ installed and accessible
- [ ] Repository cloned successfully
- [ ] Backend dependencies installed (pip install -r requirements.txt)
- [ ] Frontend dependencies installed (npm install in react-frontend/)
- [ ] Database initialized (python data/seed_beta_data.py)
- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:3000
- [ ] Can login with admin/admin123
- [ ] Can see dashboard with data
- [ ] Can view stores page

**If you checked all boxes: Congratulations! 🎉 You're all set!**

---

## 🎉 You're Ready!

You now have the Store Opening AI application running with its beautiful React.js frontend!

**What's Next?**
1. Explore the dashboard and stores
2. Try creating a new store
3. Check out the analytics (when available)
4. Read the other documentation files
5. Start customizing for your needs

---

**Version 4.0 - React Edition**  
Built with ❤️ using React, TypeScript, Material-UI, and Flask

Last Updated: February 2026
