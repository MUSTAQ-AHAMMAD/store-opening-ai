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

# Configure page with modern theme
st.set_page_config(
    page_title="Store Opening AI - Dashboard",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:5000/api"

# Enhanced Custom CSS for modern, rich UI
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Header Styles */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        text-align: center;
        animation: fadeIn 1s ease-in;
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #4a5568;
        margin: 1.5rem 0;
        border-left: 4px solid #667eea;
        padding-left: 1rem;
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .success-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .danger-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    /* Status Badges */
    .status-badge {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .status-planning {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
    }
    
    .status-in-progress {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .status-completed {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
    }
    
    .status-delayed {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
    }
    
    /* Button Styles */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Login Form Styles */
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 2.5rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    .login-header {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 2rem;
    }
    
    /* Input fields enhancement */
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Error message styling */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        padding: 1rem;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Success alert */
    div[data-baseweb="notification"][kind="success"] {
        background-color: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    
    /* Error alert */
    div[data-baseweb="notification"][kind="error"] {
        background-color: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    
    /* Warning alert */
    div[data-baseweb="notification"][kind="warning"] {
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    /* Data table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
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
    st.markdown('<div class="main-header">🏪 Store Opening AI</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="login-header">Welcome Back!</div>', unsafe_allow_html=True)
        
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
    
    # Enhanced Sidebar
    with st.sidebar:
        st.markdown(f"""
            <div style='text-align: center; padding: 25px; background: rgba(255,255,255,0.15); 
                        border-radius: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <div style='width: 70px; height: 70px; background: white; border-radius: 50%; 
                            margin: 0 auto 15px; display: flex; align-items: center; justify-content: center;
                            font-size: 2rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
                    👤
                </div>
                <h2 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>
                    {st.session_state.user.get('full_name', st.session_state.user.get('username'))}
                </h2>
                <p style='color: rgba(255,255,255,0.85); margin: 8px 0 0 0; font-size: 0.9rem;
                          background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; display: inline-block;'>
                    {st.session_state.user.get('role', 'User').replace('_', ' ').title()}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <style>
            /* Enhanced Sidebar Navigation */
            .stRadio > div {
                gap: 8px;
            }
            .stRadio > div > label {
                background: rgba(255,255,255,0.1) !important;
                padding: 12px 20px !important;
                border-radius: 10px !important;
                color: white !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
                border-left: 3px solid transparent !important;
                margin-bottom: 5px !important;
            }
            .stRadio > div > label:hover {
                background: rgba(255,255,255,0.2) !important;
                transform: translateX(5px);
                border-left: 3px solid white !important;
            }
            .stRadio > div > label[data-checked="true"] {
                background: rgba(255,255,255,0.25) !important;
                border-left: 3px solid white !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Navigation")
        
        pages = {
            "🏠 Dashboard": "dashboard",
            "🏪 Stores": "stores",
            "👥 Team Members": "team",
            "✅ Tasks & Checklists": "tasks",
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
        st.markdown("""
            <div style='color: rgba(255,255,255,0.7); font-size: 0.85rem; text-align: center;'>
                <p style='margin: 5px 0;'><strong>Store Opening AI</strong></p>
                <p style='margin: 5px 0; font-size: 0.8rem;'>Version 2.0.0</p>
                <p style='margin: 5px 0; font-size: 0.75rem;'>© 2024</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Main Content Area
    if page == "dashboard":
        st.markdown('<div class="main-header fade-in">🏠 Dashboard Overview</div>', unsafe_allow_html=True)
        
        # Fetch dashboard data
        dashboard_data = api_request("/analytics/dashboard")
        
        if dashboard_data:
            summary = dashboard_data.get('summary', {})
            
            # Key Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card success-card fade-in">
                        <h3 style='margin: 0; font-size: 2.5rem;'>{summary.get('total_stores', 0)}</h3>
                        <p style='margin: 5px 0 0 0; opacity: 0.9;'>Total Stores</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card info-card fade-in">
                        <h3 style='margin: 0; font-size: 2.5rem;'>{summary.get('total_tasks', 0)}</h3>
                        <p style='margin: 5px 0 0 0; opacity: 0.9;'>Total Tasks</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                completion_pct = 0
                if summary.get('total_tasks', 0) > 0:
                    completion_pct = (summary.get('completed_tasks', 0) / summary.get('total_tasks')) * 100
                
                st.markdown(f"""
                    <div class="metric-card warning-card fade-in">
                        <h3 style='margin: 0; font-size: 2.5rem;'>{completion_pct:.0f}%</h3>
                        <p style='margin: 5px 0 0 0; opacity: 0.9;'>Completion Rate</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-card danger-card fade-in">
                        <h3 style='margin: 0; font-size: 2.5rem;'>{summary.get('overdue_tasks', 0)}</h3>
                        <p style='margin: 5px 0 0 0; opacity: 0.9;'>Overdue Tasks</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Get AI Insights
            ai_insights_data = api_request("/ai/insights/dashboard")
            
            if ai_insights_data and ai_insights_data.get('insights'):
                st.markdown('<div class="sub-header">🤖 AI-Powered Insights</div>', unsafe_allow_html=True)
                
                for insight in ai_insights_data['insights']:
                    risk_color = {
                        'low': '🟢',
                        'medium': '🟡',
                        'high': '🔴'
                    }.get(insight['risk_level'], '⚪')
                    
                    with st.expander(f"{risk_color} {insight['store_name']} - Risk: {insight['risk_level'].upper()}", expanded=insight['risk_level'] == 'high'):
                        if insight['risk_factors']:
                            st.warning("**Risk Factors:**")
                            for factor in insight['risk_factors']:
                                st.write(f"- {factor}")
                        
                        if insight['recommendations']:
                            st.info("**AI Recommendations:**")
                            for rec in insight['recommendations']:
                                st.write(f"✓ {rec}")
                        
                        metrics = insight['metrics']
                        col_m1, col_m2, col_m3 = st.columns(3)
                        with col_m1:
                            st.metric("Completion", f"{metrics['completion_rate']}%")
                        with col_m2:
                            st.metric("Overdue", metrics['overdue_tasks'])
                        with col_m3:
                            st.metric("Days to Opening", metrics.get('days_until_opening', 'N/A'))
            
            # Store Progress Chart
            st.markdown('<div class="sub-header">📊 Store Progress Overview</div>', unsafe_allow_html=True)
            
            stores = dashboard_data.get('stores', [])
            if stores:
                df_stores = pd.DataFrame(stores)
                
                fig = px.bar(
                    df_stores,
                    x='name',
                    y='completion_percentage',
                    color='status',
                    title='Store Completion Progress',
                    labels={'completion_percentage': 'Completion %', 'name': 'Store'},
                    color_discrete_map={
                        'planning': '#ffd89b',
                        'in_progress': '#4facfe',
                        'completed': '#43e97b',
                        'delayed': '#fa709a'
                    }
                )
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', size=12)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    elif page == "ai_insights":
        st.markdown('<div class="main-header fade-in">🤖 AI-Powered Insights</div>', unsafe_allow_html=True)
        
        st.info("💡 This section provides intelligent insights powered by AI to help you make better decisions.")
        
        # Store selector
        stores_data = api_request("/stores")
        if stores_data:
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
                        
                        st.write(f"**{idx}. {priority_icon} {task.get('title')}**")
                        st.write(f"   Priority: {task.get('priority')} | Status: {task.get('status')}")
            
            with tabs[2]:
                st.subheader("Task Risk Assessment")
                st.write("Select a task to get AI-powered risk analysis:")
                
                # This would require selecting a task - simplified for now
                st.info("Feature: Analyzes historical data to predict task completion risks")
    
    elif page == "stores":
        st.markdown('<div class="main-header fade-in">🏪 Store Management</div>', unsafe_allow_html=True)
        
        # Tab layout for stores
        tab1, tab2 = st.tabs(["📋 All Stores", "➕ Add New Store"])
        
        with tab1:
            stores_data = api_request("/stores")
            
            if stores_data:
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
            else:
                st.warning("⚠️ No stores found or unable to fetch stores")
        
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
        
        if team_data:
            st.success(f"👥 Total Team Members: {len(team_data)}")
            
            # Filters
            col1, col2 = st.columns([2, 1])
            with col1:
                search_member = st.text_input("🔍 Search team members", placeholder="Search by name, email, or phone...")
            with col2:
                # Get store list for filter
                stores_data = api_request("/stores")
                store_filter_options = ["All Stores"] + [s['name'] for s in stores_data] if stores_data else ["All Stores"]
                store_filter = st.selectbox("Filter by Store", store_filter_options)
            
            st.markdown("---")
            
            # Filter team members
            filtered_team = team_data
            if search_member:
                filtered_team = [m for m in filtered_team if 
                               search_member.lower() in m.get('name', '').lower() or 
                               search_member.lower() in m.get('email', '').lower() or
                               search_member.lower() in m.get('phone', '').lower()]
            
            if store_filter != "All Stores" and stores_data:
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
                        store_name = next((s['name'] for s in stores_data if s['id'] == member.get('store_id')), 'N/A') if stores_data else 'N/A'
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
                    
                    if stores_data:
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
        st.markdown('<div class="main-header fade-in">✅ Tasks & Checklists</div>', unsafe_allow_html=True)
        
        # Store selector
        stores_data = api_request("/stores")
        if stores_data:
            col1, col2 = st.columns([2, 1])
            with col1:
                store_options = {s['name']: s['id'] for s in stores_data}
                selected_store_name = st.selectbox("Select Store", list(store_options.keys()))
                store_id = store_options[selected_store_name]
            
            with col2:
                status_filter = st.multiselect("Filter by Status", ["pending", "in_progress", "completed", "blocked"], default=["pending", "in_progress"])
            
            # Get checklists for store
            checklists_data = api_request(f"/checklists?store_id={store_id}")
            
            if checklists_data:
                for checklist in checklists_data:
                    with st.expander(f"📋 {checklist.get('name', 'Checklist')} - {checklist.get('category', 'General')}", expanded=True):
                        st.write(f"**Description:** {checklist.get('description', 'N/A')}")
                        
                        # Get tasks for this checklist
                        tasks_data = api_request(f"/checklists/{checklist['id']}/tasks")
                        
                        if tasks_data:
                            # Filter tasks
                            filtered_tasks = [t for t in tasks_data if t.get('status') in status_filter] if status_filter else tasks_data
                            
                            for task in filtered_tasks:
                                col_t1, col_t2, col_t3 = st.columns([3, 1, 1])
                                
                                with col_t1:
                                    status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "blocked": "🚫"}.get(task.get('status'), "⚪")
                                    priority_icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(task.get('priority'), "⚪")
                                    
                                    st.write(f"{status_icon} {priority_icon} **{task.get('title', 'Task')}**")
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
        else:
            st.warning("⚠️ No stores found")
    
    elif page == "whatsapp":
        st.markdown('<div class="main-header fade-in">💬 WhatsApp Management</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📱 Groups", "💬 Send Message"])
        
        with tab1:
            groups_data = api_request("/whatsapp/groups")
            
            if groups_data:
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
                if stores_data:
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
        
        with tab2:
            st.markdown("### 💬 Send WhatsApp Message")
            
            groups_data = api_request("/whatsapp/groups")
            if groups_data:
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
        st.markdown('<div class="main-header fade-in">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
        
        # Store selector
        stores_data = api_request("/stores")
        if stores_data:
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
        if stores_data:
            store_options = {s['name']: s['id'] for s in stores_data}
            selected_store = st.selectbox("Select Store", list(store_options.keys()))
            
            st.info("🔔 Select overdue tasks below to manually trigger voice escalations")
            
            # In a real implementation, we'd list overdue tasks here
            st.write("Feature: Manual voice call escalation for selected tasks")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #718096; font-size: 0.9rem;'>
            <p><strong>Store Opening AI Management System</strong> | Powered by Advanced AI & Voice Technology</p>
            <p>Secure • Intelligent • Efficient</p>
        </div>
    """, unsafe_allow_html=True)
