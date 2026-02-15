"""
Store Opening AI - AdminLTE Professional Dashboard
Modern, professional admin interface inspired by Laravel AdminLTE
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Configure page
st.set_page_config(
    page_title="Store Opening AI - Admin Panel",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api")

# AdminLTE Professional CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Global Styles */
    * {
        font-family: 'Source Sans+Pro', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Sidebar - AdminLTE Dark Style */
    [data-testid="stSidebar"] {
        background: #343a40;
        padding: 0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #343a40;
    }
    
    /* Logo Area */
    .sidebar-logo {
        background: #007bff;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0;
        border-bottom: 1px solid #4b545c;
    }
    
    .sidebar-logo h2 {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Sidebar Navigation */
    .sidebar-nav {
        padding: 0.5rem 0;
    }
    
    .nav-header {
        color: #c2c7d0;
        padding: 0.75rem 1rem;
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Navigation Buttons */
    .stButton > button {
        width: 100%;
        background: transparent;
        color: #c2c7d0;
        border: none;
        border-radius: 0;
        padding: 0.75rem 1rem;
        text-align: left;
        font-size: 0.95rem;
        font-weight: 400;
        transition: all 0.2s;
        border-left: 3px solid transparent;
    }
    
    .stButton > button:hover {
        background: #3f474e;
        color: white;
        border-left-color: #007bff;
    }
    
    .stButton > button:active,
    .stButton > button:focus {
        background: #007bff;
        color: white;
        border-left-color: #0056b3;
    }
    
    /* Main Content Area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Content Header */
    .content-header {
        background: white;
        padding: 1.5rem;
        margin: -2rem -2rem 2rem -2rem;
        border-bottom: 1px solid #dee2e6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .content-header h1 {
        font-size: 1.8rem;
        font-weight: 400;
        color: #495057;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .breadcrumb {
        display: flex;
        gap: 0.5rem;
        color: #6c757d;
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }
    
    /* Info Box (AdminLTE Style) */
    .info-box {
        display: flex;
        min-height: 90px;
        background: white;
        border-radius: 0.25rem;
        padding: 0;
        margin-bottom: 1rem;
        box-shadow: 0 0 1px rgba(0,0,0,0.125), 0 1px 3px rgba(0,0,0,0.2);
    }
    
    .info-box-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 90px;
        font-size: 2.5rem;
        border-radius: 0.25rem 0 0 0.25rem;
    }
    
    .info-box-content {
        flex: 1;
        padding: 0.75rem 1rem;
    }
    
    .info-box-text {
        font-size: 0.875rem;
        color: #6c757d;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .info-box-number {
        font-size: 1.75rem;
        font-weight: 700;
        color: #212529;
        line-height: 1;
    }
    
    .info-box-progress {
        margin-top: 0.5rem;
        font-size: 0.75rem;
        color: #6c757d;
    }
    
    /* Color Variants */
    .bg-info { background: linear-gradient(135deg, #17a2b8, #148a9c); color: white; }
    .bg-success { background: linear-gradient(135deg, #28a745, #218838); color: white; }
    .bg-warning { background: linear-gradient(135deg, #ffc107, #e0a800); color: white; }
    .bg-danger { background: linear-gradient(135deg, #dc3545, #c82333); color: white; }
    .bg-primary { background: linear-gradient(135deg, #007bff, #0056b3); color: white; }
    .bg-secondary { background: linear-gradient(135deg, #6c757d, #5a6268); color: white; }
    
    /* Card Styles */
    .card {
        background: white;
        border-radius: 0.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 1px rgba(0,0,0,0.125), 0 1px 3px rgba(0,0,0,0.2);
    }
    
    .card-header {
        background: #f8f9fa;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #dee2e6;
        border-radius: 0.25rem 0.25rem 0 0;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #495057;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-body {
        padding: 1rem;
    }
    
    .card-footer {
        background: #f8f9fa;
        padding: 0.75rem 1rem;
        border-top: 1px solid #dee2e6;
        border-radius: 0 0 0.25rem 0.25rem;
    }
    
    /* Small Box (AdminLTE) */
    .small-box {
        position: relative;
        display: block;
        border-radius: 0.25rem;
        box-shadow: 0 0 1px rgba(0,0,0,0.125), 0 1px 3px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        padding: 1.25rem;
        min-height: 120px;
    }
    
    .small-box-inner h3 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .small-box-inner p {
        font-size: 1rem;
        margin: 0;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    .small-box-icon {
        position: absolute;
        right: 1rem;
        top: 1rem;
        font-size: 4rem;
        opacity: 0.2;
    }
    
    .small-box-footer {
        display: block;
        padding: 0.5rem 0 0 0;
        margin-top: 1rem;
        text-align: center;
        font-size: 0.875rem;
        border-top: 1px solid rgba(255,255,255,0.3);
        color: rgba(255,255,255,0.8);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.25rem;
    }
    
    .badge-success { background-color: #28a745; color: white; }
    .badge-warning { background-color: #ffc107; color: #212529; }
    .badge-danger { background-color: #dc3545; color: white; }
    .badge-info { background-color: #17a2b8; color: white; }
    .badge-primary { background-color: #007bff; color: white; }
    .badge-secondary { background-color: #6c757d; color: white; }
    
    /* Buttons */
    .btn {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        font-size: 0.875rem;
        font-weight: 400;
        line-height: 1.5;
        text-align: center;
        border-radius: 0.25rem;
        transition: all 0.15s;
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    .btn-primary {
        background: #007bff;
        color: white;
        border-color: #007bff;
    }
    
    .btn-primary:hover {
        background: #0056b3;
        border-color: #004085;
    }
    
    .btn-success {
        background: #28a745;
        color: white;
        border-color: #28a745;
    }
    
    .btn-sm {
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
    }
    
    /* Alert Boxes */
    .alert {
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid transparent;
        border-radius: 0.25rem;
    }
    
    .alert-info {
        color: #0c5460;
        background-color: #d1ecf1;
        border-color: #bee5eb;
    }
    
    .alert-success {
        color: #155724;
        background-color: #d4edda;
        border-color: #c3e6cb;
    }
    
    .alert-warning {
        color: #856404;
        background-color: #fff3cd;
        border-color: #ffeaa7;
    }
    
    .alert-danger {
        color: #721c24;
        background-color: #f8d7da;
        border-color: #f5c6cb;
    }
    
    /* Tables */
    .table-responsive {
        display: block;
        width: 100%;
        overflow-x: auto;
    }
    
    /* Progress Bars */
    .progress {
        height: 1.25rem;
        background-color: #e9ecef;
        border-radius: 0.25rem;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        transition: width 0.6s ease;
    }
    
    .progress-bar-success { background: #28a745; }
    .progress-bar-warning { background: #ffc107; }
    .progress-bar-danger { background: #dc3545; }
    .progress-bar-info { background: #17a2b8; }
    
    /* Timeline (AdminLTE) */
    .timeline {
        position: relative;
        padding-left: 2rem;
    }
    
    .timeline-item {
        position: relative;
        padding-bottom: 1.5rem;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -2rem;
        top: 0;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #007bff;
        border: 2px solid white;
        box-shadow: 0 0 0 3px #007bff;
    }
    
    .timeline-item::after {
        content: '';
        position: absolute;
        left: -1.75rem;
        top: 10px;
        bottom: 0;
        width: 2px;
        background: #dee2e6;
    }
    
    .timeline-item:last-child::after {
        display: none;
    }
    
    /* AI Insight Box */
    .ai-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.4);
    }
    
    .ai-insight-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    .ai-insight-content {
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Loading Spinner */
    .spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #007bff;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Utilities */
    @media (max-width: 768px) {
        .content-header h1 {
            font-size: 1.4rem;
        }
        .info-box {
            flex-direction: column;
        }
        .info-box-icon {
            width: 100%;
            height: 60px;
            border-radius: 0.25rem 0.25rem 0 0;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def get_api_data(endpoint):
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"⚠️ API Connection Error: {str(e)}")
        return None

def post_api_data(endpoint, data):
    """Post data to API"""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=5)
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        st.error(f"⚠️ API Error: {str(e)}")
        return None

def check_test_mode():
    """Check if the system is in test mode"""
    test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
    return test_mode

# Initialize session state
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = 'dashboard'

# Sidebar - AdminLTE Style
with st.sidebar:
    # Logo Area
    st.markdown("""
        <div class="sidebar-logo">
            <h2><i class="fas fa-store"></i> Store Opening AI</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Main Navigation
    st.markdown('<div class="nav-header">Main Navigation</div>', unsafe_allow_html=True)
    
    pages = [
        {"icon": "fa-gauge", "name": "Dashboard", "key": "dashboard"},
        {"icon": "fa-store", "name": "Stores", "key": "stores"},
        {"icon": "fa-users", "name": "Team", "key": "team"},
        {"icon": "fa-list-check", "name": "Tasks", "key": "tasks"},
        {"icon": "fa-comments", "name": "Communications", "key": "communications"},
    ]
    
    for page_info in pages:
        if st.button(
            f"<i class='fas {page_info['icon']}'></i>  {page_info['name']}", 
            key=f"nav_{page_info['key']}",
            use_container_width=True
        ):
            st.session_state.selected_page = page_info['key']
            st.rerun()
    
    # Analytics Section
    st.markdown('<div class="nav-header">AI & Analytics</div>', unsafe_allow_html=True)
    
    ai_pages = [
        {"icon": "fa-brain", "name": "AI Insights", "key": "ai_insights"},
        {"icon": "fa-chart-line", "name": "Analytics", "key": "analytics"},
        {"icon": "fa-robot", "name": "ML Models", "key": "ml_models"},
    ]
    
    for page_info in ai_pages:
        if st.button(
            f"<i class='fas {page_info['icon']}'></i>  {page_info['name']}", 
            key=f"nav_{page_info['key']}",
            use_container_width=True
        ):
            st.session_state.selected_page = page_info['key']
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Test Mode Indicator
    if check_test_mode():
        st.markdown("""
            <div style="background: rgba(255, 193, 7, 0.2); padding: 0.75rem; border-radius: 0.25rem; margin-top: 1rem; border-left: 3px solid #ffc107;">
                <p style="color: #ffc107; font-weight: 600; margin: 0; font-size: 0.85rem;">
                    <i class="fas fa-flask"></i> TEST MODE
                </p>
                <p style="color: #c2c7d0; font-size: 0.75rem; margin: 0.25rem 0 0 0;">
                    Messages logged only
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Version Info
    st.markdown("""
        <div style="padding: 1rem; text-align: center; margin-top: 2rem; border-top: 1px solid #4b545c;">
            <p style="color: #6c757d; font-size: 0.75rem; margin: 0;">
                Version 3.0<br/>
                <i class="fas fa-heart" style="color: #dc3545;"></i> Built with AI
            </p>
        </div>
    """, unsafe_allow_html=True)

# Get current page
page = st.session_state.selected_page

# Main Content
if page == "dashboard":
    # Content Header
    st.markdown("""
        <div class="content-header">
            <h1><i class="fas fa-gauge"></i> Dashboard</h1>
            <div class="breadcrumb">
                <span><i class="fas fa-home"></i> Home</span>
                <span>/</span>
                <span>Dashboard</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Fetch dashboard data
    with st.spinner("Loading dashboard..."):
        dashboard_data = get_api_data("/analytics/dashboard")
        ml_insights = get_api_data("/ml/insights/success-factors")
    
    if dashboard_data:
        summary = dashboard_data.get('summary', {})
        
        # Small Boxes (AdminLTE Style)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="small-box bg-info">
                    <div class="small-box-inner">
                        <h3>{summary.get('total_stores', 0)}</h3>
                        <p>Total Stores</p>
                    </div>
                    <div class="small-box-icon">
                        <i class="fas fa-store"></i>
                    </div>
                    <div class="small-box-footer">
                        {summary.get('active_stores', 0)} Active
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            completion_rate = (summary.get('completed_tasks', 0) / max(summary.get('total_tasks', 1), 1)) * 100
            st.markdown(f"""
                <div class="small-box bg-success">
                    <div class="small-box-inner">
                        <h3>{completion_rate:.0f}%</h3>
                        <p>Completion Rate</p>
                    </div>
                    <div class="small-box-icon">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <div class="small-box-footer">
                        {summary.get('completed_tasks', 0)} / {summary.get('total_tasks', 0)} Tasks
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="small-box bg-warning">
                    <div class="small-box-inner">
                        <h3>{summary.get('overdue_tasks', 0)}</h3>
                        <p>Overdue Tasks</p>
                    </div>
                    <div class="small-box-icon">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div class="small-box-footer">
                        Needs Attention
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="small-box bg-danger">
                    <div class="small-box-inner">
                        <h3>{summary.get('critical_priority_tasks', 0)}</h3>
                        <p>Critical Tasks</p>
                    </div>
                    <div class="small-box-icon">
                        <i class="fas fa-fire"></i>
                    </div>
                    <div class="small-box-footer">
                        High Priority
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # AI Insights Section
        if ml_insights and ml_insights.get('insights'):
            st.markdown("""
                <div class="ai-insight">
                    <div class="ai-insight-header">
                        <i class="fas fa-brain"></i>
                        AI-Powered Insights
                    </div>
                    <div class="ai-insight-content">
            """, unsafe_allow_html=True)
            
            for insight in ml_insights['insights'][:3]:
                st.markdown(f"• {insight}")
            
            st.markdown(f"""
                        <div style="margin-top: 0.75rem; font-size: 0.85rem; opacity: 0.9;">
                            <i class="fas fa-database"></i> Based on {ml_insights.get('data_points', 0)} completed stores
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Row 2: Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">
                            <i class="fas fa-chart-bar"></i> Store Progress
                        </div>
                    </div>
                    <div class="card-body">
            """, unsafe_allow_html=True)
            
            stores = dashboard_data.get('stores', [])
            if stores:
                df_stores = pd.DataFrame(stores)
                fig = px.bar(
                    df_stores,
                    x='name',
                    y='completion_percentage',
                    color='status',
                    title='',
                    color_discrete_map={
                        'planning': '#ffc107',
                        'in_progress': '#17a2b8',
                        'completed': '#28a745',
                        'delayed': '#dc3545'
                    }
                )
                fig.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">
                            <i class="fas fa-chart-pie"></i> Task Distribution
                        </div>
                    </div>
                    <div class="card-body">
            """, unsafe_allow_html=True)
            
            task_data = {
                'Status': ['Completed', 'Pending', 'Overdue'],
                'Count': [
                    summary.get('completed_tasks', 0),
                    summary.get('pending_tasks', 0),
                    summary.get('overdue_tasks', 0)
                ]
            }
            df_tasks = pd.DataFrame(task_data)
            
            fig = px.pie(
                df_tasks,
                values='Count',
                names='Status',
                title='',
                color='Status',
                color_discrete_map={
                    'Completed': '#28a745',
                    'Pending': '#17a2b8',
                    'Overdue': '#dc3545'
                }
            )
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Upcoming Openings
        st.markdown("""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fas fa-calendar-days"></i> Upcoming Store Openings
                    </div>
                </div>
                <div class="card-body">
        """, unsafe_allow_html=True)
        
        upcoming = dashboard_data.get('upcoming_openings', [])
        if upcoming:
            for opening in upcoming:
                opening_date = datetime.fromisoformat(opening['opening_date'].replace('Z', '+00:00'))
                days = opening.get('days_until_opening', 0)
                
                # Color code based on days
                if days <= 7:
                    badge_class = 'badge-danger'
                elif days <= 14:
                    badge_class = 'badge-warning'
                else:
                    badge_class = 'badge-info'
                
                st.markdown(f"""
                    <div style="padding: 0.75rem; border-bottom: 1px solid #dee2e6;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong><i class="fas fa-store"></i> {opening['name']}</strong>
                                <div style="color: #6c757d; font-size: 0.875rem; margin-top: 0.25rem;">
                                    <i class="fas fa-map-marker-alt"></i> {opening['location']}
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <span class="badge {badge_class}">{days} days</span>
                                <div style="color: #6c757d; font-size: 0.875rem; margin-top: 0.25rem;">
                                    {opening_date.strftime('%b %d, %Y')}
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> No upcoming openings in the next 30 days
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

elif page == "stores":
    st.markdown("""
        <div class="content-header">
            <h1><i class="fas fa-store"></i> Store Management</h1>
            <div class="breadcrumb">
                <span><i class="fas fa-home"></i> Home</span>
                <span>/</span>
                <span>Stores</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add Store Button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("➕ Add New Store", use_container_width=True):
            st.session_state.show_add_store = True
    
    # Add Store Form
    if st.session_state.get('show_add_store', False):
        st.markdown("""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fas fa-plus"></i> Create New Store
                    </div>
                </div>
                <div class="card-body">
        """, unsafe_allow_html=True)
        
        with st.form("add_store_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Store Name *", placeholder="Enter store name")
                opening_date = st.date_input("Opening Date *", min_value=datetime.now().date())
            with col2:
                location = st.text_input("Location *", placeholder="City, State")
                status = st.selectbox("Status", ["planning", "in_progress", "completed", "delayed"])
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                submitted = st.form_submit_button("✅ Create Store", use_container_width=True)
            with col2:
                cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submitted and name and location:
                data = {
                    'name': name,
                    'location': location,
                    'opening_date': opening_date.isoformat(),
                    'status': status
                }
                result = post_api_data("/stores", data)
                if result:
                    st.success(f"✅ Store '{name}' created successfully!")
                    st.session_state.show_add_store = False
                    st.rerun()
            
            if cancelled:
                st.session_state.show_add_store = False
                st.rerun()
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display Stores
    with st.spinner("Loading stores..."):
        stores = get_api_data("/stores")
    
    if stores:
        st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fas fa-list"></i> All Stores ({len(stores)})
                    </div>
                </div>
                <div class="card-body">
        """, unsafe_allow_html=True)
        
        for store in stores:
            with st.expander(f"🏪 {store['name']} - {store['location']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    status_map = {
                        'planning': ('badge-warning', 'Planning'),
                        'in_progress': ('badge-info', 'In Progress'),
                        'completed': ('badge-success', 'Completed'),
                        'delayed': ('badge-danger', 'Delayed')
                    }
                    badge_class, status_text = status_map.get(store['status'], ('badge-secondary', store['status']))
                    
                    st.markdown(f"""
                        <div>
                            <strong>Status:</strong>
                            <span class="badge {badge_class}">{status_text}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    opening_date = datetime.fromisoformat(store['opening_date'].replace('Z', '+00:00'))
                    st.write(f"**📅 Opening:** {opening_date.strftime('%b %d, %Y')}")
                
                with col2:
                    store_details = get_api_data(f"/stores/{store['id']}")
                    if store_details:
                        st.write(f"**👥 Team:** {store_details.get('team_members_count', 0)} members")
                        st.write(f"**📝 Tasks:** {store_details.get('total_tasks', 0)}")
                
                with col3:
                    if store_details:
                        completion = store_details.get('completion_percentage', 0)
                        st.write(f"**✅ Progress:** {completion:.0f}%")
                        st.progress(completion / 100)
                
                # Actions
                if st.button(f"👁️ View Details", key=f"view_{store['id']}", use_container_width=True):
                    st.session_state.selected_store = store['id']
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

elif page == "ai_insights":
    st.markdown("""
        <div class="content-header">
            <h1><i class="fas fa-brain"></i> AI-Powered Insights</h1>
            <div class="breadcrumb">
                <span><i class="fas fa-home"></i> Home</span>
                <span>/</span>
                <span>AI Insights</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load AI insights
    with st.spinner("Loading AI insights..."):
        ml_insights = get_api_data("/ml/insights/success-factors")
        ai_insights = get_api_data("/ai/insights/dashboard")
    
    # Success Factors
    if ml_insights and ml_insights.get('insights'):
        st.markdown("""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fas fa-lightbulb"></i> Success Factors Analysis
                    </div>
                </div>
                <div class="card-body">
        """, unsafe_allow_html=True)
        
        for insight in ml_insights['insights']:
            st.markdown(f"""
                <div style="padding: 0.75rem; background: #f8f9fa; border-left: 4px solid #007bff; margin-bottom: 0.75rem; border-radius: 0.25rem;">
                    {insight}
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
                    <div style="margin-top: 1rem; color: #6c757d; font-size: 0.875rem;">
                        <i class="fas fa-database"></i> Analysis based on {ml_insights.get('data_points', 0)} completed stores
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Store Risk Assessment
    if ai_insights and ai_insights.get('insights'):
        st.markdown("""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fas fa-exclamation-triangle"></i> Risk Assessment
                    </div>
                </div>
                <div class="card-body">
        """, unsafe_allow_html=True)
        
        for store_insight in ai_insights['insights']:
            risk_color = {
                'high': '#dc3545',
                'medium': '#ffc107',
                'low': '#28a745'
            }
            color = risk_color.get(store_insight['risk_level'], '#6c757d')
            
            st.markdown(f"""
                <div style="padding: 1rem; border-left: 4px solid {color}; background: white; margin-bottom: 1rem; border-radius: 0.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <h4 style="margin: 0 0 0.5rem 0; color: #495057;">
                        <i class="fas fa-store"></i> {store_insight['store_name']}
                    </h4>
                    <div style="margin-bottom: 0.75rem;">
                        <span class="badge badge-{store_insight['risk_level']}" style="background: {color};">
                            {store_insight['risk_level'].upper()} RISK
                        </span>
                    </div>
            """, unsafe_allow_html=True)
            
            if store_insight.get('risk_factors'):
                st.markdown("**Risk Factors:**")
                for factor in store_insight['risk_factors']:
                    st.markdown(f"• {factor}")
            
            if store_insight.get('recommendations'):
                st.markdown("**Recommendations:**")
                for rec in store_insight['recommendations']:
                    st.markdown(f"✓ {rec}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

elif page == "ml_models":
    st.markdown("""
        <div class="content-header">
            <h1><i class="fas fa-robot"></i> Machine Learning Models</h1>
            <div class="breadcrumb">
                <span><i class="fas fa-home"></i> Home</span>
                <span>/</span>
                <span>ML Models</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load model stats
    with st.spinner("Loading ML models..."):
        model_stats = get_api_data("/ml/models/stats")
    
    if model_stats:
        models = model_stats.get('models', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Completion Predictor
            comp_model = models.get('completion_predictor', {})
            st.markdown(f"""
                <div class="info-box">
                    <div class="info-box-icon bg-info">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="info-box-content">
                        <div class="info-box-text">Completion Predictor</div>
                        <div class="info-box-number">{comp_model.get('accuracy', 0):.1%}</div>
                        <div class="info-box-progress">
                            {'✅ Trained' if comp_model.get('trained') else '⏳ Training'} • {comp_model.get('data_points', 0)} samples
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Risk Assessor
            risk_model = models.get('risk_assessor', {})
            st.markdown(f"""
                <div class="info-box">
                    <div class="info-box-icon bg-danger">
                        <i class="fas fa-shield-halved"></i>
                    </div>
                    <div class="info-box-content">
                        <div class="info-box-text">Risk Assessor</div>
                        <div class="info-box-number">{risk_model.get('data_points', 0)}</div>
                        <div class="info-box-progress">
                            {'✅ Active' if risk_model.get('trained') else '⏳ Learning'} • Patterns identified
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Task Duration Predictor
            duration_model = models.get('task_duration', {})
            st.markdown(f"""
                <div class="info-box">
                    <div class="info-box-icon bg-success">
                        <i class="fas fa-clock"></i>
                    </div>
                    <div class="info-box-content">
                        <div class="info-box-text">Task Duration Predictor</div>
                        <div class="info-box-number">{duration_model.get('task_types', 0)}</div>
                        <div class="info-box-progress">
                            {'✅ Trained' if duration_model.get('trained') else '⏳ Training'} • {duration_model.get('total_samples', 0)} samples
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Success Factors
            success_model = models.get('success_factors', {})
            st.markdown(f"""
                <div class="info-box">
                    <div class="info-box-icon bg-warning">
                        <i class="fas fa-trophy"></i>
                    </div>
                    <div class="info-box-content">
                        <div class="info-box-text">Success Factor Analysis</div>
                        <div class="info-box-number">{success_model.get('data_points', 0)}</div>
                        <div class="info-box-progress">
                            {'✅ Patterns Found' if success_model.get('patterns_identified') else '⏳ Analyzing'}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Training Controls
        st.markdown("""
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fas fa-gears"></i> Model Training & Management
                    </div>
                </div>
                <div class="card-body">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Train from Completed Stores", use_container_width=True):
                with st.spinner("Training models..."):
                    result = post_api_data("/ml/batch-learn", {})
                    if result:
                        st.success(f"✅ Trained on {result.get('stores_processed', 0)} stores!")
                        st.rerun()
        
        with col2:
            st.markdown("""
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Models automatically learn from each completed store opening
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

# Add similar pages for other sections...

# Footer
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #6c757d; font-size: 0.875rem; border-top: 1px solid #dee2e6; margin-top: 3rem;">
        <p style="margin: 0;"><strong>Store Opening AI Management System</strong> v3.0</p>
        <p style="margin: 0.25rem 0 0 0;">Powered by Self-Learning AI • Built with <i class="fas fa-heart" style="color: #dc3545;"></i></p>
    </div>
""", unsafe_allow_html=True)
