"""
Store Opening AI - Enhanced Dashboard with Authentication
Modern, Rich UI with User Management and AI Features
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Constants
TARGET_COMPLETION_RATE = 80
RISK_THRESHOLD_HIGH = 75
RISK_STATUS_CRITICAL = 5
RISK_STATUS_MODERATE = 0

# Configure page with modern theme
st.set_page_config(
    page_title="Store Opening AI - Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:5000/api"

# Enhanced Custom CSS for modern, professional admin panel UI
st.markdown("""
    <style>
    /* CSS Variables for Professional Theme */
    :root {
        --primary-color: #2563eb;
        --primary-hover: #1d4ed8;
        --primary-light: #dbeafe;
        --success-color: #059669;
        --warning-color: #d97706;
        --danger-color: #dc2626;
        --info-color: #0891b2;
        --light-bg: #f9fafb;
        --card-bg: #ffffff;
        --text-primary: #111827;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Global Styles with professional system fonts */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Main container - Professional flat design */
    .main {
        background: var(--light-bg);
        padding: 0;
    }
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        background: transparent;
        max-width: 1400px;
    }
    
    /* Header Styles - Clean and Professional */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        text-align: left;
    }
    
    .page-subtitle {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        text-align: left;
    }
    
    .sub-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    /* Professional Metric Cards */
    .metric-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    .metric-card-icon {
        width: 48px;
        height: 48px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-card-primary .metric-card-icon {
        background: var(--primary-color);
        color: white;
    }
    
    .metric-card-success .metric-card-icon {
        background: var(--success-color);
        color: white;
    }
    
    .metric-card-warning .metric-card-icon {
        background: var(--warning-color);
        color: white;
    }
    
    .metric-card-danger .metric-card-icon {
        background: var(--danger-color);
        color: white;
    }
    
    .metric-card-info .metric-card-icon {
        background: var(--info-color);
        color: white;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-trend {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .metric-trend-up {
        color: var(--success-color);
    }
    
    .metric-trend-down {
        color: var(--danger-color);
    }
    
    /* Executive Summary Banner */
    .executive-banner {
        background: var(--primary-color);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
    }
    
    /* Professional Header */
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    /* Risk Pills */
    .risk-pill {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .risk-pill-high {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .risk-pill-medium {
        background: #fef3c7;
        color: #92400e;
    }
    
    .risk-pill-low {
        background: #d1fae5;
        color: #065f46;
    }
    
    /* Enhanced Insight Boxes */
    .insight-box {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .insight-box-warning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
    
    .insight-box-info {
        background: #dbeafe;
        border-left: 4px solid #3b82f6;
    }
    
    .insight-box-success {
        background: #d1fae5;
        border-left: 4px solid #10b981;
    }
    
    /* Professional Status Badges */
    .status-badge {
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-planning {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .status-in-progress {
        background: #fef3c7;
        color: #92400e;
    }
    
    .status-completed {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-delayed {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Button Styles - Modern and Clean */
    .stButton>button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .stButton>button:hover {
        background: var(--primary-hover);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    /* Sidebar Styles - Professional Navigation */
    [data-testid="stSidebar"] {
        background: var(--card-bg);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: var(--text-primary);
    }
    
    /* Sidebar User Profile Section */
    .user-profile-card {
        background: var(--primary-color);
        padding: 1.25rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .user-profile-icon {
        width: 56px;
        height: 56px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        margin: 0 auto 0.75rem;
        border: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    .user-profile-name {
        font-size: 1.125rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .user-profile-role {
        font-size: 0.875rem;
        opacity: 0.9;
    }
    
    /* Login Form Styles - Professional */
    .login-container {
        max-width: 420px;
        margin: 0 auto;
        padding: 2.5rem;
        background: var(--card-bg);
        border-radius: 16px;
        box-shadow: var(--shadow-xl);
        border: 1px solid var(--border-color);
    }
    
    .login-header {
        text-align: center;
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        text-align: center;
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    /* Input fields enhancement */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 0.625rem;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        background: var(--card-bg);
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* Card Container for Content */
    .content-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
    }
    
    .content-card-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* Alert Styling - Professional */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 0.875rem;
    }
    
    /* Progress bar - Modern */
    .stProgress > div > div > div {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    /* Data Tables - Professional */
    .dataframe {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px;
        overflow: hidden;
        font-size: 0.875rem;
    }
    
    .dataframe th {
        background: var(--light-bg) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        padding: 0.75rem !important;
    }
    
    .dataframe td {
        padding: 0.75rem !important;
        border-bottom: 1px solid var(--border-color) !important;
    }
    
    .dataframe tr:hover {
        background: var(--light-bg) !important;
    }
    
    /* Tabs - Modern Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 0;
        padding: 0.75rem 1.25rem;
        font-weight: 500;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary-color) !important;
        border-bottom-color: var(--primary-color) !important;
    }
    
    /* Expander - Professional */
    .streamlit-expanderHeader {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--light-bg);
        border-color: var(--primary-color);
    }
    
    /* Metrics from Streamlit */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Navigation Menu Styling */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.25rem;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: var(--primary-light);
        color: var(--primary-color);
        border-color: var(--primary-color);
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] > div:first-child {
        display: none;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label > div {
        color: inherit;
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + div + div {
        background: var(--primary-light);
        color: var(--primary-color);
        border-color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Hide default radio button circles */
    [data-testid="stSidebar"] .stRadio [role="radio"] {
        display: none;
    }
    
    /* Style for active navigation item */
    [data-testid="stSidebar"] .stRadio input[type="radio"]:checked ~ label,
    [data-testid="stSidebar"] .stRadio input[type="radio"]:checked + div {
        background: var(--primary-light) !important;
        color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
        font-weight: 600 !important;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-in;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'token' not in st.session_state:
    st.session_state.token = None

# Helper functions
def api_request(endpoint, method='GET', data=None, auth_required=True, handle_session_expiry=True):
    """Make API request with authentication"""
    headers = {}
    
    if auth_required and st.session_state.token:
        headers['Authorization'] = f'Bearer {st.session_state.token}'
    
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 401:
            # Only handle as session expiry if we're authenticated and it's not a login attempt
            if handle_session_expiry and st.session_state.authenticated:
                st.session_state.authenticated = False
                st.session_state.token = None
                st.session_state.user = None
                st.error("🔒 Your session has expired. Please login again to continue.")
            return None
        elif response.status_code >= 400:
            # Try to get error message from response
            try:
                error_data = response.json()
                error_msg = error_data.get('error', f'API Error: {response.status_code}')
                return {'error': error_msg}
            except:
                return {'error': f'API Error: {response.status_code}'}
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    
    except requests.exceptions.ConnectionError:
        st.error(f"⚠️ Connection Error: Unable to reach the server. Please check if the backend is running.")
        return None
    except requests.exceptions.Timeout:
        st.error(f"⚠️ Request Timeout: The server is taking too long to respond. Please try again.")
        return None
    except Exception as e:
        # Log the actual error for debugging
        print(f"API Request Error: {str(e)}")
        st.error(f"⚠️ An unexpected error occurred. Please try again.")
        return None

def login(username, password):
    """Login user"""
    data = {'username': username, 'password': password}
    result = api_request('/auth/login', method='POST', data=data, auth_required=False, handle_session_expiry=False)
    
    if result:
        st.session_state.authenticated = True
        st.session_state.token = result.get('token')
        st.session_state.user = result.get('user')
        return True
    return False

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user = None
    st.rerun()

# Login Page
if not st.session_state.authenticated:
    st.markdown('<div class="main-header">Store Opening AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Professional Store Management Platform</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="login-header">Welcome Back</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Sign in to access your dashboard</div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                login_button = st.form_submit_button("Login", use_container_width=True)
            
            with col_btn2:
                register_button = st.form_submit_button("Register", use_container_width=True)
            
            if login_button:
                if username and password:
                    if login(username, password):
                        st.success("✅ Login successful! Welcome back.")
                        st.rerun()
                    else:
                        st.error("🔐 Invalid username or password. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password")
            
            if register_button:
                st.session_state.show_register = True
                st.rerun()
        
        # Registration form
        if st.session_state.get('show_register', False):
            st.markdown("---")
            st.markdown("### Create New Account")
            
            with st.form("register_form"):
                new_username = st.text_input("Choose Username")
                new_email = st.text_input("Email Address")
                new_password = st.text_input("Choose Password", type="password")
                new_full_name = st.text_input("Full Name")
                
                col_reg1, col_reg2 = st.columns(2)
                
                with col_reg1:
                    register_submit = st.form_submit_button("Create Account", use_container_width=True)
                
                with col_reg2:
                    cancel_register = st.form_submit_button("Cancel", use_container_width=True)
                
                if register_submit:
                    if new_username and new_email and new_password:
                        reg_data = {
                            'username': new_username,
                            'email': new_email,
                            'password': new_password,
                            'full_name': new_full_name,
                            'role': 'team_member'
                        }
                        result = api_request('/auth/register', method='POST', data=reg_data, auth_required=False, handle_session_expiry=False)
                        
                        if result and 'error' not in result:
                            st.success("✅ Account created successfully! Please login with your credentials.")
                            st.session_state.show_register = False
                            st.rerun()
                        elif result and 'error' in result:
                            # Show specific error message from API
                            st.error(f"❌ Registration failed: {result['error']}")
                        else:
                            st.error("❌ Registration failed. Please try again.")
                    else:
                        st.warning("⚠️ Please fill in all required fields (Username, Email, and Password)")
                
                if cancel_register:
                    st.session_state.show_register = False
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("**Demo Credentials:** Use the registration form to create an account, or contact your administrator.")

else:
    # Main Dashboard (Authenticated)
    
    # Professional Sidebar
    with st.sidebar:
        # User Profile Card
        st.markdown(f"""
            <div class="user-profile-card fade-in">
                <div class="user-profile-icon">👤</div>
                <div class="user-profile-name">
                    {st.session_state.user.get('full_name', st.session_state.user.get('username'))}
                </div>
                <div class="user-profile-role">
                    {st.session_state.user.get('role', 'User').replace('_', ' ').title()}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu
        st.markdown("### Navigation")
        
        pages = {
            "🏠 Dashboard": "dashboard",
            "🏪 Stores": "stores",
            "👥 Team Members": "team",
            "☑ Tasks & Checklists": "tasks",
            "💬 WhatsApp": "whatsapp",
            "📊 Analytics": "analytics",
            "🤖 AI Insights": "ai_insights",
            "📞 Voice Escalations": "voice"
        }
        
        selected_page = st.radio("", list(pages.keys()), label_visibility="collapsed")
        page = pages[selected_page]
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
            <div style='color: var(--text-secondary); font-size: 0.75rem; text-align: center;'>
                <p style='margin: 5px 0;'><strong>Store Opening AI</strong></p>
                <p style='margin: 5px 0;'>Version 2.0.0</p>
                <p style='margin: 5px 0;'>© 2024</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Main Content Area
    if page == "dashboard":
        # Executive Header with Date
        current_date = datetime.now().strftime("%B %d, %Y")
        st.markdown(f'''
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <div>
                    <div class="main-header">Executive Dashboard</div>
                    <div class="page-subtitle">Real-time insights and performance metrics</div>
                </div>
                <div style="text-align: right; color: var(--text-secondary); font-size: 0.875rem;">
                    <div style="font-weight: 600; color: var(--text-primary);">{current_date}</div>
                    <div>Last updated: Just now</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        # Fetch dashboard data
        dashboard_data = api_request("/analytics/dashboard")
        
        if dashboard_data:
            summary = dashboard_data.get('summary', {})
            
            # Executive Summary Card
            st.markdown(f"""
                <div style="background: #2563eb; 
                            padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 0.875rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                                System Status
                            </div>
                            <div style="font-size: 1.5rem; font-weight: 700;">
                                {"🟢 All Systems Operational" if summary.get('overdue_tasks', 0) < 3 else "⚠️ Attention Required"}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 0.25rem;">Overall Progress</div>
                            <div style="font-size: 2rem; font-weight: 700;">{(summary.get('completed_tasks', 0) / max(summary.get('total_tasks', 1), 1) * 100):.0f}%</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Key Metrics Row with Professional Cards and Trends
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card metric-card-primary fade-in">
                        <div class="metric-card-icon">🏪</div>
                        <div class="metric-value">{summary.get('total_stores', 0)}</div>
                        <div class="metric-label">Active Stores</div>
                        <div class="metric-trend metric-trend-up" style="margin-top: 0.5rem; font-size: 0.8rem;">
                            <span style="color: #10b981;">▲ 2</span> vs last period
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card metric-card-info fade-in">
                        <div class="metric-card-icon">📋</div>
                        <div class="metric-value">{summary.get('total_tasks', 0)}</div>
                        <div class="metric-label">Total Tasks</div>
                        <div style="margin-top: 0.5rem; font-size: 0.8rem; color: var(--text-secondary);">
                            {summary.get('completed_tasks', 0)} completed
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                completion_pct = 0
                if summary.get('total_tasks', 0) > 0:
                    completion_pct = (summary.get('completed_tasks', 0) / summary.get('total_tasks')) * 100
                
                trend_color = "#10b981" if completion_pct >= RISK_THRESHOLD_HIGH else "#f59e0b"
                st.markdown(f"""
                    <div class="metric-card metric-card-success fade-in">
                        <div class="metric-card-icon">✓</div>
                        <div class="metric-value">{completion_pct:.1f}%</div>
                        <div class="metric-label">Completion Rate</div>
                        <div class="metric-trend" style="margin-top: 0.5rem; font-size: 0.8rem; color: {trend_color};">
                            Target: {TARGET_COMPLETION_RATE}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                overdue = summary.get('overdue_tasks', 0)
                status_color = "#ef4444" if overdue > RISK_STATUS_CRITICAL else "#f59e0b" if overdue > RISK_STATUS_MODERATE else "#10b981"
                st.markdown(f"""
                    <div class="metric-card metric-card-danger fade-in">
                        <div class="metric-card-icon">⚠</div>
                        <div class="metric-value">{overdue}</div>
                        <div class="metric-label">Overdue Tasks</div>
                        <div style="margin-top: 0.5rem; font-size: 0.8rem;">
                            <span style="color: {status_color}; font-weight: 600;">
                                {"Critical" if overdue > RISK_STATUS_CRITICAL else "Moderate" if overdue > RISK_STATUS_MODERATE else "Good"}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Get AI Insights
            ai_insights_data = api_request("/ai/insights/dashboard")
            
            if ai_insights_data and ai_insights_data.get('insights'):
                st.markdown('''
                    <div class="sub-header">
                        <span style="margin-right: 0.5rem;">🎯</span>
                        Strategic Insights & Risk Assessment
                    </div>
                ''', unsafe_allow_html=True)
                
                # Count insights by risk level
                risk_counts = {'high': 0, 'medium': 0, 'low': 0}
                for insight in ai_insights_data['insights']:
                    risk_level = insight.get('risk_level', 'low')
                    risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
                
                # Risk Summary Pills
                if risk_counts['high'] > 0 or risk_counts['medium'] > 0:
                    st.markdown(f"""
                        <div style="display: flex; gap: 0.75rem; margin-bottom: 1rem; flex-wrap: wrap;">
                            {f'<div style="background: #fee2e2; color: #991b1b; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; font-size: 0.875rem;">🔴 {risk_counts["high"]} High Risk</div>' if risk_counts['high'] > 0 else ''}
                            {f'<div style="background: #fef3c7; color: #92400e; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; font-size: 0.875rem;">🟡 {risk_counts["medium"]} Medium Risk</div>' if risk_counts['medium'] > 0 else ''}
                            {f'<div style="background: #d1fae5; color: #065f46; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; font-size: 0.875rem;">🟢 {risk_counts["low"]} Low Risk</div>' if risk_counts['low'] > 0 else ''}
                        </div>
                    """, unsafe_allow_html=True)
                
                for insight in ai_insights_data['insights']:
                    risk_color = {
                        'low': '🟢',
                        'medium': '🟡',
                        'high': '🔴'
                    }.get(insight['risk_level'], '⚪')
                    
                    with st.expander(f"{risk_color} {insight['store_name']} - Risk: {insight['risk_level'].upper()}", expanded=insight['risk_level'] == 'high'):
                        if insight['risk_factors']:
                            st.markdown("""
                                <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 1rem;">
                                    <div style="font-weight: 600; color: #92400e; margin-bottom: 0.5rem;">⚠️ Risk Factors:</div>
                            """, unsafe_allow_html=True)
                            for factor in insight['risk_factors']:
                                st.write(f"• {factor}")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        if insight['recommendations']:
                            st.markdown("""
                                <div style="background: #dbeafe; padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 1rem;">
                                    <div style="font-weight: 600; color: #1e40af; margin-bottom: 0.5rem;">💡 Recommended Actions:</div>
                            """, unsafe_allow_html=True)
                            for rec in insight['recommendations']:
                                st.write(f"✓ {rec}")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        metrics = insight['metrics']
                        col_m1, col_m2, col_m3 = st.columns(3)
                        with col_m1:
                            st.metric("Completion", f"{metrics['completion_rate']}%", 
                                     delta=f"{metrics['completion_rate'] - 75}%" if metrics['completion_rate'] < 100 else "Complete")
                        with col_m2:
                            st.metric("Overdue Tasks", metrics['overdue_tasks'],
                                     delta=f"-{metrics['overdue_tasks']}" if metrics['overdue_tasks'] > 0 else "On Track",
                                     delta_color="inverse")
                        with col_m3:
                            days_until = metrics.get('days_until_opening', 'N/A')
                            st.metric("Days to Opening", days_until,
                                     delta="Urgent" if isinstance(days_until, int) and days_until < 7 else "")
            
            # Store Progress Chart
            st.markdown('''
                <div class="sub-header">
                    <span style="margin-right: 0.5rem;">📈</span>
                    Store Performance Analytics
                </div>
            ''', unsafe_allow_html=True)
            
            stores = dashboard_data.get('stores', [])
            if stores:
                df_stores = pd.DataFrame(stores)
                
                # Enhanced chart with professional styling
                fig = px.bar(
                    df_stores,
                    x='name',
                    y='completion_percentage',
                    color='status',
                    title='',
                    labels={'completion_percentage': 'Completion %', 'name': 'Store Location'},
                    color_discrete_map={
                        'planning': '#60a5fa',
                        'in_progress': '#f59e0b',
                        'completed': '#10b981',
                        'delayed': '#ef4444'
                    },
                    text='completion_percentage'
                )
                
                # Professional chart styling
                fig.update_traces(
                    texttemplate='%{text:.1f}%',
                    textposition='outside',
                    marker_line_color='rgba(255,255,255,0.3)',
                    marker_line_width=2
                )
                
                fig.update_layout(
                    height=450,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='-apple-system, BlinkMacSystemFont, Segoe UI, Roboto', size=13, color='#1e293b'),
                    xaxis=dict(
                        showgrid=False,
                        showline=True,
                        linecolor='#e2e8f0',
                        linewidth=2,
                        title_font=dict(size=14, color='#475569'),
                        tickfont=dict(size=12, color='#64748b')
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='#f1f5f9',
                        showline=False,
                        title_font=dict(size=14, color='#475569'),
                        tickfont=dict(size=12, color='#64748b'),
                        range=[0, 110]
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        bgcolor='rgba(255,255,255,0.9)',
                        bordercolor='#e2e8f0',
                        borderwidth=1,
                        font=dict(size=12)
                    ),
                    margin=dict(t=50, b=50, l=50, r=50),
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True, key="store_progress_chart")
                
                # Add export button
                col_export1, col_export2, col_export3 = st.columns([1, 1, 2])
                with col_export1:
                    if st.button("📊 Export Chart Data", use_container_width=True):
                        csv = df_stores.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"store_progress_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                        )
                with col_export2:
                    if st.button("📄 Generate Report", use_container_width=True):
                        st.info("Report generation feature - Coming soon")
    
    
    elif page == "ai_insights":
        st.markdown('<div class="main-header fade-in">🤖 AI-Powered Insights</div>', unsafe_allow_html=True)
        
        st.info("💡 This section provides intelligent insights powered by AI to help you make better decisions.")
        
        # Store selector
        stores_data = api_request("/stores")
        if stores_data and isinstance(stores_data, list):
            store_options = {s['name']: s['id'] for s in stores_data}
            selected_store_name = st.selectbox("Select Store for Analysis", list(store_options.keys()))
            store_id = store_options[selected_store_name]
            
            tabs = st.tabs(["📈 Completion Prediction", "🎯 Task Prioritization", "⚠️ Risk Assessment"])
            
            with tabs[0]:
                st.subheader("Completion Date Prediction")
                prediction_data = api_request(f"/ai/predict/completion-date/{store_id}")
                
                if prediction_data:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Opening Date", prediction_data.get('opening_date', 'N/A')[:10] if prediction_data.get('opening_date') else 'N/A')
                    with col2:
                        st.metric("Predicted Completion", prediction_data.get('predicted_completion', 'N/A')[:10] if prediction_data.get('predicted_completion') else 'N/A')
                    with col3:
                        on_track = prediction_data.get('on_track', False)
                        st.metric("Status", "✅ On Track" if on_track else "⚠️ At Risk")
                    
                    metrics = prediction_data.get('metrics', {})
                    st.write("**Performance Metrics:**")
                    st.write(f"- Remaining Tasks: {metrics.get('remaining_tasks', 0)}")
                    st.write(f"- Average Tasks/Day: {metrics.get('average_tasks_per_day', 0)}")
                    st.write(f"- Tasks Completed (Last 14 Days): {metrics.get('tasks_completed_last_14_days', 0)}")
            
            with tabs[1]:
                st.subheader("AI-Suggested Task Prioritization")
                prioritization_data = api_request(f"/ai/store/{store_id}/task-prioritization")
                
                if prioritization_data and prioritization_data.get('tasks'):
                    st.success(f"🎯 AI Analysis Complete - {len(prioritization_data['tasks'])} tasks analyzed")
                    
                    tasks = prioritization_data['tasks']
                    for idx, task in enumerate(tasks[:5], 1):
                        priority_icon = {
                            'critical': '🔴',
                            'high': '🟠',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(task.get('priority'), '⚪')
                        
                        st.markdown(f"**{idx}. {priority_icon} {task.get('title')}**", unsafe_allow_html=True)
                        st.write(f"   Priority: {task.get('priority')} | Status: {task.get('status')}")
            
            with tabs[2]:
                st.subheader("Task Risk Assessment")
                st.write("Select a task to get AI-powered risk analysis:")
                
                # This would require selecting a task - simplified for now
                st.info("Feature: Analyzes historical data to predict task completion risks")
        elif stores_data and isinstance(stores_data, dict) and 'error' in stores_data:
            st.error(f"⚠️ Error loading stores: {stores_data['error']}")
        else:
            st.warning("⚠️ Unable to load stores. Please check if the backend is running.")
    
    elif page == "stores":
        st.markdown('<div class="main-header fade-in">🏪 Store Management</div>', unsafe_allow_html=True)
        
        # Tab layout for stores
        tab1, tab2 = st.tabs(["📋 All Stores", "➕ Add New Store"])
        
        with tab1:
            stores_data = api_request("/stores")
            
            if stores_data and isinstance(stores_data, list):
                st.success(f"📊 Total Stores: {len(stores_data)}")
                
                # Filters
                col1, col2 = st.columns([2, 1])
                with col1:
                    search_term = st.text_input("🔍 Search stores", placeholder="Search by name or location...")
                with col2:
                    status_filter = st.selectbox("Filter by Status", ["All", "planning", "in_progress", "completed", "delayed"])
                
                # Filter stores
                filtered_stores = stores_data
                if search_term:
                    filtered_stores = [s for s in filtered_stores if search_term.lower() in s.get('name', '').lower() or search_term.lower() in s.get('location', '').lower()]
                if status_filter != "All":
                    filtered_stores = [s for s in filtered_stores if s.get('status') == status_filter]
                
                st.markdown("---")
                
                # Display stores in grid
                for store in filtered_stores:
                    with st.expander(f"🏪 {store['name']} - {store.get('location', 'N/A')}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            status_class = f"status-{store.get('status', 'planning')}"
                            st.markdown(f'<span class="status-badge {status_class}">{store.get("status", "planning").upper()}</span>', unsafe_allow_html=True)
                            st.write(f"**Opening Date:** {store.get('opening_date', 'N/A')[:10] if store.get('opening_date') else 'N/A'}")
                        
                        with col2:
                            st.write(f"**Manager:** {store.get('manager', 'N/A')}")
                            st.write(f"**Size:** {store.get('size', 'N/A')} sq ft")
                        
                        with col3:
                            completion = store.get('completion_percentage', 0)
                            st.metric("Completion", f"{completion}%")
                            st.progress(completion / 100)
                        
                        # Action buttons
                        col_a1, col_a2, col_a3 = st.columns(3)
                        
                        with col_a1:
                            if st.button(f"📝 Edit", key=f"edit_{store['id']}"):
                                st.session_state.edit_store_id = store['id']
                                st.rerun()
                        
                        with col_a2:
                            if st.button(f"📊 View Details", key=f"view_{store['id']}"):
                                st.session_state.view_store_id = store['id']
                                st.rerun()
                        
                        with col_a3:
                            if st.button(f"🗑️ Delete", key=f"delete_{store['id']}", type="secondary"):
                                result = api_request(f"/stores/{store['id']}", method='DELETE')
                                if result:
                                    st.success("✅ Store deleted successfully!")
                                    st.rerun()
                
                # Edit Store Modal
                if st.session_state.get('edit_store_id'):
                    st.markdown("---")
                    st.markdown("### 📝 Edit Store")
                    
                    store_to_edit = next((s for s in stores_data if s['id'] == st.session_state.edit_store_id), None)
                    
                    if store_to_edit:
                        with st.form("edit_store_form"):
                            edit_name = st.text_input("Store Name", value=store_to_edit.get('name', ''))
                            edit_location = st.text_input("Location", value=store_to_edit.get('location', ''))
                            edit_size = st.number_input("Size (sq ft)", value=store_to_edit.get('size', 0))
                            edit_manager = st.text_input("Manager", value=store_to_edit.get('manager', ''))
                            edit_status = st.selectbox("Status", ["planning", "in_progress", "completed", "delayed"], 
                                                      index=["planning", "in_progress", "completed", "delayed"].index(store_to_edit.get('status', 'planning')))
                            edit_opening_date = st.date_input("Opening Date", value=datetime.strptime(store_to_edit.get('opening_date', datetime.now().isoformat())[:10], '%Y-%m-%d') if store_to_edit.get('opening_date') else datetime.now())
                            
                            col_edit1, col_edit2 = st.columns(2)
                            with col_edit1:
                                save_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                            with col_edit2:
                                cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
                            
                            if save_edit:
                                update_data = {
                                    'name': edit_name,
                                    'location': edit_location,
                                    'size': edit_size,
                                    'manager': edit_manager,
                                    'status': edit_status,
                                    'opening_date': edit_opening_date.isoformat()
                                }
                                result = api_request(f"/stores/{st.session_state.edit_store_id}", method='PUT', data=update_data)
                                if result and 'error' not in result:
                                    st.success("✅ Store updated successfully!")
                                    del st.session_state.edit_store_id
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update store")
                            
                            if cancel_edit:
                                del st.session_state.edit_store_id
                                st.rerun()
            elif stores_data and isinstance(stores_data, dict) and 'error' in stores_data:
                st.error(f"⚠️ Error loading stores: {stores_data['error']}")
            else:
                st.info("📭 No stores found. Add a new store to get started!")
        
        with tab2:
            st.markdown("### ➕ Create New Store")
            
            with st.form("add_store_form"):
                new_name = st.text_input("Store Name*", placeholder="e.g., Downtown Seattle Store")
                new_location = st.text_input("Location*", placeholder="e.g., 123 Main St, Seattle, WA")
                
                col1, col2 = st.columns(2)
                with col1:
                    new_size = st.number_input("Size (sq ft)*", min_value=0, value=5000)
                    new_manager = st.text_input("Manager Name", placeholder="e.g., John Doe")
                
                with col2:
                    new_status = st.selectbox("Status", ["planning", "in_progress", "completed", "delayed"])
                    new_opening_date = st.date_input("Opening Date", value=datetime.now() + timedelta(days=90))
                
                new_description = st.text_area("Description", placeholder="Additional notes about the store...")
                
                submit_new = st.form_submit_button("✅ Create Store", use_container_width=True)
                
                if submit_new:
                    if new_name and new_location and new_size:
                        store_data = {
                            'name': new_name,
                            'location': new_location,
                            'size': new_size,
                            'manager': new_manager,
                            'status': new_status,
                            'opening_date': new_opening_date.isoformat(),
                            'description': new_description
                        }
                        result = api_request("/stores", method='POST', data=store_data)
                        if result and 'error' not in result:
                            st.success("✅ Store created successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to create store: {result.get('error', 'Unknown error')}")
                    else:
                        st.warning("⚠️ Please fill in all required fields (Name, Location, Size)")
    
    elif page == "team":
        st.markdown('<div class="main-header fade-in">👥 Team Management</div>', unsafe_allow_html=True)
        
        team_data = api_request("/team")
        
        if team_data and isinstance(team_data, list):
            st.success(f"👥 Total Team Members: {len(team_data)}")
            
            # Filters
            col1, col2 = st.columns([2, 1])
            with col1:
                search_member = st.text_input("🔍 Search team members", placeholder="Search by name, email, or phone...")
            with col2:
                # Get store list for filter
                stores_data = api_request("/stores")
                store_filter_options = ["All Stores"] + [s['name'] for s in stores_data] if stores_data and isinstance(stores_data, list) else ["All Stores"]
                store_filter = st.selectbox("Filter by Store", store_filter_options)
            
            st.markdown("---")
            
            # Filter team members
            filtered_team = team_data
            if search_member:
                filtered_team = [m for m in filtered_team if 
                               search_member.lower() in m.get('name', '').lower() or 
                               search_member.lower() in m.get('email', '').lower() or
                               search_member.lower() in m.get('phone', '').lower()]
            
            if store_filter != "All Stores" and stores_data and isinstance(stores_data, list):
                store_id = next((s['id'] for s in stores_data if s['name'] == store_filter), None)
                if store_id:
                    filtered_team = [m for m in filtered_team if m.get('store_id') == store_id]
            
            # Display as cards
            for member in filtered_team:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### 👤 {member.get('name', 'N/A')}")
                        st.write(f"**Role:** {member.get('role', 'N/A')}")
                    
                    with col2:
                        st.write(f"📧 {member.get('email', 'N/A')}")
                        st.write(f"📱 {member.get('phone', 'N/A')}")
                    
                    with col3:
                        store_name = next((s['name'] for s in stores_data if s['id'] == member.get('store_id')), 'N/A') if stores_data and isinstance(stores_data, list) else 'N/A'
                        st.write(f"🏪 **Store:**")
                        st.write(store_name)
                    
                    with col4:
                        if st.button("📝 Edit", key=f"edit_member_{member['id']}"):
                            st.session_state.edit_member_id = member['id']
                            st.rerun()
                        if st.button("🗑️ Delete", key=f"delete_member_{member['id']}"):
                            result = api_request(f"/team/{member['id']}", method='DELETE')
                            if result:
                                st.success("✅ Member removed!")
                                st.rerun()
                    
                    st.markdown("---")
            
            # Add new team member
            with st.expander("➕ Add New Team Member"):
                with st.form("add_member_form"):
                    new_member_name = st.text_input("Name*")
                    new_member_email = st.text_input("Email*")
                    new_member_phone = st.text_input("Phone*")
                    new_member_role = st.selectbox("Role", ["team_member", "manager", "admin"])
                    
                    if stores_data and isinstance(stores_data, list):
                        store_options = {s['name']: s['id'] for s in stores_data}
                        new_member_store = st.selectbox("Assign to Store", list(store_options.keys()))
                        new_member_store_id = store_options[new_member_store]
                    else:
                        new_member_store_id = None
                    
                    submit_member = st.form_submit_button("✅ Add Member", use_container_width=True)
                    
                    if submit_member:
                        if new_member_name and new_member_email and new_member_phone:
                            member_data = {
                                'name': new_member_name,
                                'email': new_member_email,
                                'phone': new_member_phone,
                                'role': new_member_role,
                                'store_id': new_member_store_id
                            }
                            result = api_request("/team", method='POST', data=member_data)
                            if result and 'error' not in result:
                                st.success("✅ Team member added!")
                                st.rerun()
                            else:
                                st.error(f"❌ Failed to add member: {result.get('error', 'Unknown error')}")
                        else:
                            st.warning("⚠️ Please fill in required fields")
        else:
            st.warning("⚠️ No team members found")
    
    elif page == "tasks":
        st.markdown('<div class="main-header fade-in">☑ Tasks & Checklists</div>', unsafe_allow_html=True)
        
        # Store selector
        stores_data = api_request("/stores")
        if stores_data and isinstance(stores_data, list):
            col1, col2 = st.columns([2, 1])
            with col1:
                store_options = {s['name']: s['id'] for s in stores_data}
                selected_store_name = st.selectbox("Select Store", list(store_options.keys()))
                store_id = store_options[selected_store_name]
            
            with col2:
                status_filter = st.multiselect("Filter by Status", ["pending", "in_progress", "completed", "blocked"], default=["pending", "in_progress"])
            
            # Get checklists for store
            checklists_data = api_request(f"/checklists?store_id={store_id}")
            
            if checklists_data and isinstance(checklists_data, list):
                for checklist in checklists_data:
                    with st.expander(f"📋 {checklist.get('name', 'Checklist')} - {checklist.get('category', 'General')}", expanded=True):
                        st.write(f"**Description:** {checklist.get('description', 'N/A')}")
                        
                        # Get tasks for this checklist
                        tasks_data = api_request(f"/checklists/{checklist['id']}/tasks")
                        
                        if tasks_data and isinstance(tasks_data, list):
                            # Filter tasks
                            filtered_tasks = [t for t in tasks_data if t.get('status') in status_filter] if status_filter else tasks_data
                            
                            for task in filtered_tasks:
                                col_t1, col_t2, col_t3 = st.columns([3, 1, 1])
                                
                                with col_t1:
                                    status_icon = {
                                        "pending": '⏳',
                                        "in_progress": '🔄',
                                        "completed": '✅',
                                        "blocked": '🚫'
                                    }.get(task.get('status'), '⚪')
                                    priority_icon = {
                                        "low": '🟢',
                                        "medium": '🟡',
                                        "high": '🟠',
                                        "critical": '🔴'
                                    }.get(task.get('priority'), '⚪')
                                    
                                    st.markdown(f"{status_icon} {priority_icon} **{task.get('title', 'Task')}**", unsafe_allow_html=True)
                                    if task.get('description'):
                                        st.caption(task.get('description'))
                                
                                with col_t2:
                                    if task.get('due_date'):
                                        due_date = datetime.strptime(task['due_date'][:10], '%Y-%m-%d')
                                        days_until = (due_date - datetime.now()).days
                                        
                                        if days_until < 0:
                                            st.error(f"🔴 Overdue by {abs(days_until)} days")
                                        elif days_until == 0:
                                            st.warning("⚠️ Due Today")
                                        elif days_until <= 3:
                                            st.warning(f"📅 Due in {days_until} days")
                                        else:
                                            st.info(f"📅 Due: {task['due_date'][:10]}")
                                
                                with col_t3:
                                    new_status = st.selectbox("Status", ["pending", "in_progress", "completed", "blocked"], 
                                                            index=["pending", "in_progress", "completed", "blocked"].index(task.get('status', 'pending')),
                                                            key=f"task_status_{task['id']}")
                                    
                                    if new_status != task.get('status'):
                                        update_result = api_request(f"/checklists/tasks/{task['id']}", 
                                                                   method='PUT', 
                                                                   data={'status': new_status})
                                        if update_result:
                                            st.success("✅ Status updated!")
                                            st.rerun()
                                
                                st.markdown("---")
                        else:
                            st.info("No tasks in this checklist")
            else:
                st.info("No checklists found for this store")
                
                # Option to create checklist
                with st.expander("➕ Create New Checklist"):
                    with st.form("new_checklist_form"):
                        checklist_name = st.text_input("Checklist Name*")
                        checklist_category = st.selectbox("Category", ["Construction", "Permits", "Equipment", "Staffing", "Marketing", "Other"])
                        checklist_desc = st.text_area("Description")
                        
                        submit_checklist = st.form_submit_button("Create Checklist")
                        
                        if submit_checklist:
                            if checklist_name:
                                checklist_data = {
                                    'name': checklist_name,
                                    'category': checklist_category,
                                    'description': checklist_desc,
                                    'store_id': store_id
                                }
                                result = api_request("/checklists", method='POST', data=checklist_data)
                                if result and 'error' not in result:
                                    st.success("✅ Checklist created!")
                                    st.rerun()
        elif stores_data and isinstance(stores_data, dict) and 'error' in stores_data:
            st.error(f"⚠️ Error loading stores: {stores_data['error']}")
        else:
            st.warning("⚠️ No stores found")
    
    elif page == "whatsapp":
        st.markdown('<div class="main-header fade-in">💬 WhatsApp Management</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📱 Groups", "💬 Send Message"])
        
        with tab1:
            groups_data = api_request("/whatsapp/groups")
            
            if groups_data and isinstance(groups_data, list):
                st.success(f"📱 Total WhatsApp Groups: {len(groups_data)}")
                
                for group in groups_data:
                    with st.expander(f"💬 {group.get('name', 'Group')} - {group.get('store_name', 'N/A')}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Group ID:** {group.get('group_id', 'N/A')}")
                            st.write(f"**Store:** {group.get('store_name', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Created:** {group.get('created_at', 'N/A')[:10] if group.get('created_at') else 'N/A'}")
                            st.write(f"**Active:** {'✅ Yes' if group.get('is_active') else '❌ No'}")
                        
                        with col3:
                            if st.button(f"📤 Send Message", key=f"send_msg_{group['id']}"):
                                st.session_state.selected_group_id = group['id']
                                st.session_state.show_send_message = True
                                st.rerun()
                        
                        # Show message archive
                        archive_data = api_request(f"/whatsapp/groups/{group['id']}/archive")
                        if archive_data and archive_data.get('messages'):
                            st.markdown("**Recent Messages:**")
                            for msg in archive_data['messages'][:5]:
                                st.caption(f"📅 {msg.get('sent_at', 'N/A')[:16] if msg.get('sent_at') else 'N/A'}")
                                st.text(msg.get('message', 'N/A'))
                                st.markdown("---")
            else:
                st.info("No WhatsApp groups found")
            
            # Create new group
            with st.expander("➕ Create New WhatsApp Group"):
                stores_data = api_request("/stores")
                if stores_data and isinstance(stores_data, list):
                    with st.form("create_whatsapp_group"):
                        store_options = {s['name']: s['id'] for s in stores_data}
                        selected_store = st.selectbox("Select Store", list(store_options.keys()))
                        group_name = st.text_input("Group Name*")
                        group_id = st.text_input("WhatsApp Group ID*", placeholder="e.g., 120363XXXXX@g.us")
                        
                        submit_group = st.form_submit_button("Create Group")
                        
                        if submit_group:
                            if group_name and group_id:
                                group_data = {
                                    'store_id': store_options[selected_store],
                                    'name': group_name,
                                    'group_id': group_id
                                }
                                result = api_request("/whatsapp/groups", method='POST', data=group_data)
                                if result and 'error' not in result:
                                    st.success("✅ WhatsApp group created!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to create group")
                elif stores_data and isinstance(stores_data, dict) and 'error' in stores_data:
                    st.error(f"⚠️ Error loading stores: {stores_data['error']}")
                else:
                    st.warning("⚠️ No stores found")
        
        with tab2:
            st.markdown("### 💬 Send WhatsApp Message")
            
            groups_data = api_request("/whatsapp/groups")
            if groups_data and isinstance(groups_data, list):
                group_options = {f"{g['name']} - {g.get('store_name', 'N/A')}": g['id'] for g in groups_data}
                selected_group = st.selectbox("Select Group", list(group_options.keys()))
                
                message_type = st.radio("Message Type", ["Custom Message", "Task Follow-up"])
                
                if message_type == "Custom Message":
                    message_content = st.text_area("Message", height=150, placeholder="Type your message here...")
                    
                    if st.button("📤 Send Message", use_container_width=True):
                        if message_content:
                            group_id = group_options[selected_group]
                            result = api_request(f"/whatsapp/groups/{group_id}/send", 
                                               method='POST', 
                                               data={'message': message_content})
                            if result and 'error' not in result:
                                st.success("✅ Message sent successfully!")
                            else:
                                st.error("❌ Failed to send message")
                        else:
                            st.warning("⚠️ Please enter a message")
                
                else:
                    st.info("Select a task to send automated follow-up")
                    # This would integrate with tasks
            else:
                st.warning("⚠️ No WhatsApp groups available")
    
    elif page == "analytics":
        st.markdown('<div class="main-header fade-in">📈 Analytics Dashboard</div>', unsafe_allow_html=True)
        
        # Store selector
        stores_data = api_request("/stores")
        if stores_data and isinstance(stores_data, list):
            store_options = {"All Stores": None}
            store_options.update({s['name']: s['id'] for s in stores_data})
            selected_store = st.selectbox("Select Store", list(store_options.keys()))
            store_id = store_options[selected_store]
            
            if store_id:
                # Individual store analytics
                progress_data = api_request(f"/analytics/store/{store_id}/progress")
                
                if progress_data:
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Overall Progress", f"{progress_data.get('overall_progress', 0)}%")
                    with col2:
                        st.metric("Total Tasks", progress_data.get('total_tasks', 0))
                    with col3:
                        st.metric("Completed", progress_data.get('completed_tasks', 0))
                    with col4:
                        st.metric("Overdue", progress_data.get('overdue_tasks', 0))
                    
                    st.markdown("---")
                    
                    # Progress by category
                    if progress_data.get('progress_by_category'):
                        st.subheader("📊 Progress by Category")
                        
                        categories = progress_data['progress_by_category']
                        df_cat = pd.DataFrame([
                            {'Category': cat, 'Completed': data['completed'], 'Total': data['total'], 
                             'Percentage': (data['completed'] / data['total'] * 100) if data['total'] > 0 else 0}
                            for cat, data in categories.items()
                        ])
                        
                        fig = px.bar(df_cat, x='Category', y='Percentage', 
                                    title='Completion Rate by Category',
                                    color='Percentage',
                                    color_continuous_scale='Viridis')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Task status distribution
                    if progress_data.get('task_status_distribution'):
                        st.subheader("📈 Task Status Distribution")
                        
                        status_dist = progress_data['task_status_distribution']
                        df_status = pd.DataFrame(list(status_dist.items()), columns=['Status', 'Count'])
                        
                        fig = px.pie(df_status, values='Count', names='Status',
                                    title='Task Distribution by Status',
                                    color_discrete_sequence=px.colors.sequential.Viridis)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Timeline
                    if progress_data.get('timeline'):
                        st.subheader("📅 Progress Timeline")
                        
                        timeline = progress_data['timeline']
                        df_timeline = pd.DataFrame([
                            {'Date': entry['date'], 'Completed': entry['completed']}
                            for entry in timeline
                        ])
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=df_timeline['Date'], y=df_timeline['Completed'],
                                                mode='lines+markers',
                                                name='Completed Tasks',
                                                line=dict(color='#667eea', width=3)))
                        fig.update_layout(title='Tasks Completed Over Time',
                                        xaxis_title='Date',
                                        yaxis_title='Tasks Completed')
                        st.plotly_chart(fig, use_container_width=True)
            else:
                # Overall analytics
                dashboard_data = api_request("/analytics/dashboard")
                
                if dashboard_data:
                    summary = dashboard_data.get('summary', {})
                    
                    # Overall metrics
                    st.subheader("🎯 Overall Performance")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Stores", summary.get('total_stores', 0))
                    with col2:
                        st.metric("Total Tasks", summary.get('total_tasks', 0))
                    with col3:
                        completion_rate = (summary.get('completed_tasks', 0) / summary.get('total_tasks', 1)) * 100
                        st.metric("Completion Rate", f"{completion_rate:.1f}%")
                    with col4:
                        st.metric("Overdue Tasks", summary.get('overdue_tasks', 0))
                    
                    st.markdown("---")
                    
                    # Store comparison
                    stores = dashboard_data.get('stores', [])
                    if stores:
                        st.subheader("🏪 Store Comparison")
                        
                        df_stores = pd.DataFrame(stores)
                        
                        fig = px.bar(df_stores, x='name', y='completion_percentage',
                                    color='status',
                                    title='Store Progress Comparison',
                                    labels={'completion_percentage': 'Completion %', 'name': 'Store'})
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Status distribution
                        status_counts = df_stores['status'].value_counts()
                        fig2 = px.pie(values=status_counts.values, names=status_counts.index,
                                     title='Store Status Distribution')
                        st.plotly_chart(fig2, use_container_width=True)
        elif stores_data and isinstance(stores_data, dict) and 'error' in stores_data:
            st.error(f"⚠️ Error loading stores: {stores_data['error']}")
        else:
            st.warning("⚠️ No stores found")
    
    elif page == "voice":
        st.markdown('<div class="main-header fade-in">📞 Voice Escalation System</div>', unsafe_allow_html=True)
        
        st.success("🎯 AI-powered voice calling for critical task escalations")
        
        st.markdown("### How It Works")
        st.write("""
        The voice escalation system automatically calls team members and managers when:
        - Tasks are overdue by 3+ days (Level 1 Escalation)
        - Tasks are overdue by 7+ days (Level 2 - Manager Escalation)
        - Critical priority tasks miss deadlines
        """)
        
        st.markdown("### Manual Escalation")
        
        stores_data = api_request("/stores")
        if stores_data and isinstance(stores_data, list):
            store_options = {s['name']: s['id'] for s in stores_data}
            selected_store = st.selectbox("Select Store", list(store_options.keys()))
            
            st.info("🔔 Select overdue tasks below to manually trigger voice escalations")
            
            # In a real implementation, we'd list overdue tasks here
            st.write("Feature: Manual voice call escalation for selected tasks")
        elif stores_data and isinstance(stores_data, dict) and 'error' in stores_data:
            st.error(f"⚠️ Error loading stores: {stores_data['error']}")
        else:
            st.warning("⚠️ No stores found")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #718096; font-size: 0.9rem;'>
            <p><strong>Store Opening AI Management System</strong> | Powered by Advanced AI & Voice Technology</p>
            <p>Secure • Intelligent • Efficient</p>
        </div>
    """, unsafe_allow_html=True)
