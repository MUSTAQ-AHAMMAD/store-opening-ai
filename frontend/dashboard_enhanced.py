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
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
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
    
    /* Alert boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #667eea;
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
def api_request(endpoint, method='GET', data=None, auth_required=True):
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
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.user = None
            st.error("Session expired. Please login again.")
            return None
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def login(username, password):
    """Login user"""
    data = {'username': username, 'password': password}
    result = api_request('/auth/login', method='POST', data=data, auth_required=False)
    
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
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please enter both username and password")
            
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
                        result = api_request('/auth/register', method='POST', data=reg_data, auth_required=False)
                        
                        if result:
                            st.success("Account created successfully! Please login.")
                            st.session_state.show_register = False
                            st.rerun()
                    else:
                        st.warning("Please fill in all required fields")
                
                if cancel_register:
                    st.session_state.show_register = False
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("**Demo Credentials:** Use the registration form to create an account, or contact your administrator.")

else:
    # Main Dashboard (Authenticated)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 20px;'>
                <h2 style='color: white; margin: 0;'>👤 {st.session_state.user.get('full_name', st.session_state.user.get('username'))}</h2>
                <p style='color: rgba(255,255,255,0.8); margin: 5px 0;'>{st.session_state.user.get('role', 'User').replace('_', ' ').title()}</p>
            </div>
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
            <div style='color: rgba(255,255,255,0.6); font-size: 0.85rem; text-align: center;'>
                <p><strong>Store Opening AI</strong></p>
                <p>Version 2.0.0</p>
                <p>© 2024</p>
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
                    completion_pct = (summary.get('completed_tasks', 0) / summary.get('total_tasks', 1)) * 100
                
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
