# Frontend Migration: Streamlit → React.js

## 🎉 Welcome to the New React Frontend!

This project has been **upgraded from Streamlit to React.js** for the frontend dashboard. The new React frontend provides a modern, responsive, and beautiful user interface built with TypeScript and Material-UI.

## 📦 What Changed?

### Before (Streamlit)
- Python-based dashboard in `frontend/` directory
- Port: 8501
- Command: `streamlit run frontend/dashboard.py`

### After (React.js)
- Modern React.js + TypeScript dashboard in `react-frontend/` directory
- Port: 3000
- Command: `./start_dashboard.sh` (or `start_dashboard.bat` on Windows)

## 🚀 Getting Started

### Prerequisites
- **Python 3.9+** (for backend)
- **Node.js 14+** and npm (for React frontend)

### Quick Setup

1. **Run the setup script** (installs both Python and React dependencies):
   ```bash
   ./setup.sh  # Mac/Linux
   # or
   setup.bat   # Windows
   ```

2. **Start the backend** (Terminal 1):
   ```bash
   python main.py
   ```

3. **Start the React dashboard** (Terminal 2):
   ```bash
   ./start_dashboard.sh  # Mac/Linux
   # or
   start_dashboard.bat   # Windows
   ```

4. **Access the dashboard**:
   - Open http://localhost:3000 in your browser
   - Login with: `admin` / `admin123`

## ✨ New Features

The React frontend includes:
- 🎨 **Modern UI**: Beautiful purple gradient theme with Material-UI components
- ⚡ **Fast Performance**: Client-side rendering for instant navigation
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- 🔐 **Secure Authentication**: Token-based login with protected routes
- 💎 **TypeScript**: Full type safety for better development experience
- 🎯 **Intuitive Navigation**: Clean sidebar with easy access to all features

## 📚 Documentation

For detailed information, see:
- [REACT_QUICKSTART.md](./REACT_QUICKSTART.md) - Quick start guide
- [REACT_FRONTEND_GUIDE.md](./REACT_FRONTEND_GUIDE.md) - Complete frontend documentation
- [README.md](./README.md) - Main project documentation

## 🗂️ Old Streamlit Frontend

The old Streamlit frontend files are still in the `frontend/` directory for reference, but they are **no longer used or maintained**. All documentation and scripts have been updated to use the new React frontend.

If you need the Streamlit version for any reason, you can:
1. Install Streamlit: `pip install streamlit>=1.39.0`
2. Run it manually: `streamlit run frontend/dashboard.py`

However, we **strongly recommend** using the new React frontend for the best experience.

## ❓ Questions?

If you have any questions or issues with the new React frontend, please:
1. Check the [REACT_QUICKSTART.md](./REACT_QUICKSTART.md) guide
2. Review the troubleshooting sections in [LOCAL_TESTING_GUIDE.md](./LOCAL_TESTING_GUIDE.md)
3. Open an issue on GitHub

---

**Enjoy the new React frontend! 🎉**
