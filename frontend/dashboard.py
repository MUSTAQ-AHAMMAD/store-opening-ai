"""
Store Opening AI Management System - Improved Dashboard
Modern, professional web interface with better UI/UX
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
    page_title="Store Opening AI Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api")

# Enhanced Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: white;
        font-weight: 500;
    }
    
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }
    
    /* Page title styling */
    .page-title {
        font-size: 2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .page-subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.35rem 1rem;
        border-radius: 2rem;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        text-transform: uppercase;
    }
    
    .status-planning {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #78350f;
    }
    
    .status-in-progress {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        color: white;
    }
    
    .status-completed {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
        color: white;
    }
    
    .status-delayed {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
        color: white;
    }
    
    /* Nav button styling */
    .nav-button {
        width: 100%;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border: none;
        border-radius: 0.5rem;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        text-align: left;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    .nav-button.active {
        background: rgba(255, 255, 255, 0.25);
        border-left: 4px solid #fbbf24;
    }
    
    /* Test mode banner */
    .test-mode-banner {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        color: #78350f;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(251, 191, 36, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    /* Card container */
    .card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .card:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Form styling */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 0.5rem;
        border: 2px solid #e5e7eb;
        transition: border-color 0.2s;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.75rem;
        }
        .page-title {
            font-size: 1.5rem;
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

def put_api_data(endpoint, data):
    """Update data via API"""
    try:
        response = requests.put(f"{API_BASE_URL}{endpoint}", json=data, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"⚠️ API Error: {str(e)}")
        return None

def check_test_mode():
    """Check if the system is in test mode"""
    # Try to get from environment or default to False
    test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
    return test_mode

def format_status_badge(status):
    """Format status as HTML badge"""
    status_lower = status.lower().replace(' ', '-')
    return f'<span class="status-badge status-{status_lower}">{status.upper()}</span>'

# Initialize session state
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = 'dashboard'

# Sidebar navigation with improved UI
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <h1 style="color: white; font-size: 1.75rem; font-weight: 700; margin: 0;">
                🏢 Store Opening AI
            </h1>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                Management System
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation menu with icons
    pages = [
        {"icon": "🏠", "name": "Dashboard", "key": "dashboard"},
        {"icon": "🏪", "name": "Stores", "key": "stores"},
        {"icon": "👥", "name": "Team Members", "key": "team"},
        {"icon": "✅", "name": "Tasks & Checklists", "key": "tasks"},
        {"icon": "💬", "name": "Communications", "key": "whatsapp"},
        {"icon": "📊", "name": "Analytics & Reports", "key": "analytics"},
    ]
    
    st.markdown('<p style="color: rgba(255,255,255,0.9); font-weight: 600; margin-bottom: 0.5rem;">NAVIGATION</p>', unsafe_allow_html=True)
    
    for page_info in pages:
        if st.button(
            f"{page_info['icon']}  {page_info['name']}", 
            key=f"nav_{page_info['key']}",
            use_container_width=True
        ):
            st.session_state.selected_page = page_info['key']
            st.rerun()
    
    st.markdown("---")
    
    # Test mode indicator in sidebar
    if check_test_mode():
        st.markdown("""
            <div style="background: rgba(251, 191, 36, 0.2); padding: 0.75rem; border-radius: 0.5rem; border-left: 4px solid #fbbf24;">
                <p style="color: #fbbf24; font-weight: 600; margin: 0; font-size: 0.85rem;">
                    🧪 TEST MODE ACTIVE
                </p>
                <p style="color: rgba(255,255,255,0.8); font-size: 0.75rem; margin: 0.25rem 0 0 0;">
                    Messages are logged, not sent
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System info
    st.markdown("""
        <div style="padding: 0.5rem; text-align: center;">
            <p style="color: rgba(255,255,255,0.6); font-size: 0.75rem; margin: 0;">
                Version 3.0<br/>
                © 2024 Store Opening AI
            </p>
        </div>
    """, unsafe_allow_html=True)

# Get current page
page = st.session_state.selected_page

# Show test mode banner at top if in test mode
if check_test_mode():
    st.markdown("""
        <div class="test-mode-banner">
            <span style="font-size: 1.5rem;">🧪</span>
            <span>TEST MODE: All messages (WhatsApp, SMS, Voice, Email) are logged to console only. No actual messages will be sent.</span>
        </div>
    """, unsafe_allow_html=True)

# Main content based on selected page
if page == "dashboard":
    st.markdown('<div class="page-title">🏠 Dashboard Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Welcome to your Store Opening Management System</div>', unsafe_allow_html=True)
    
    # Fetch dashboard data
    with st.spinner("Loading dashboard data..."):
        dashboard_data = get_api_data("/analytics/dashboard")
    
    if dashboard_data:
        summary = dashboard_data.get('summary', {})
        
        # Key metrics with enhanced cards
        st.markdown("### 📈 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📦 Total Stores",
                value=summary.get('total_stores', 0),
                delta=None
            )
            st.metric(
                label="🚀 Active Stores",
                value=summary.get('active_stores', 0),
                delta=None
            )
        
        with col2:
            st.metric(
                label="📝 Total Tasks",
                value=summary.get('total_tasks', 0),
                delta=None
            )
            st.metric(
                label="✅ Completed Tasks",
                value=summary.get('completed_tasks', 0),
                delta=f"{summary.get('completed_tasks', 0)} completed"
            )
        
        with col3:
            st.metric(
                label="⏳ Pending Tasks",
                value=summary.get('pending_tasks', 0),
                delta=None
            )
            st.metric(
                label="⚠️ Overdue Tasks",
                value=summary.get('overdue_tasks', 0),
                delta=f"{summary.get('overdue_tasks', 0)} overdue",
                delta_color="inverse"
            )
        
        with col4:
            st.metric(
                label="🔴 High Priority",
                value=summary.get('high_priority_tasks', 0),
                delta=None
            )
            st.metric(
                label="🚨 Critical Priority",
                value=summary.get('critical_priority_tasks', 0),
                delta=f"{summary.get('critical_priority_tasks', 0)} critical",
                delta_color="inverse"
            )
        
        st.markdown("---")
        
        # Upcoming openings
        st.markdown("### 📅 Upcoming Store Openings (Next 30 Days)")
        upcoming = dashboard_data.get('upcoming_openings', [])
        
        if upcoming:
            for opening in upcoming:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    with col1:
                        st.markdown(f"**🏪 {opening['name']}**")
                    with col2:
                        st.write(f"📍 {opening['location']}")
                    with col3:
                        opening_date = datetime.fromisoformat(opening['opening_date'].replace('Z', '+00:00'))
                        st.write(f"📆 {opening_date.strftime('%Y-%m-%d')}")
                    with col4:
                        days = opening.get('days_until_opening', 0)
                        st.write(f"⏱️ {days} days")
                st.markdown("---")
        else:
            st.info("ℹ️ No upcoming openings in the next 30 days")
        
        # Store progress overview
        st.markdown("### 📊 Store Progress Overview")
        stores = dashboard_data.get('stores', [])
        
        if stores:
            df_stores = pd.DataFrame(stores)
            
            # Completion chart
            fig = px.bar(
                df_stores,
                x='name',
                y='completion_percentage',
                color='status',
                title='Store Completion Progress',
                labels={'completion_percentage': 'Completion %', 'name': 'Store Name'},
                color_discrete_map={
                    'planning': '#fbbf24',
                    'in_progress': '#3b82f6',
                    'completed': '#10b981',
                    'delayed': '#ef4444'
                }
            )
            fig.update_layout(
                height=400,
                font=dict(family="Inter, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Store details table
            st.dataframe(
                df_stores[['name', 'status', 'total_tasks', 'completed_tasks', 'completion_percentage']],
                use_container_width=True,
                hide_index=True
            )
    else:
        st.warning("⚠️ Unable to load dashboard data. Please ensure the API server is running.")

elif page == "stores":
    st.markdown('<div class="page-title">🏪 Store Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Manage your store openings and track progress</div>', unsafe_allow_html=True)
    
    # Add new store button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("➕ Add New Store", use_container_width=True):
            st.session_state.show_add_store = True
    
    # Add store form
    if st.session_state.get('show_add_store', False):
        with st.form("add_store_form", clear_on_submit=True):
            st.markdown("### ➕ Create New Store")
            
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
    
    st.markdown("---")
    
    # Display stores
    with st.spinner("Loading stores..."):
        stores = get_api_data("/stores")
    
    if stores:
        st.markdown(f"### 📋 All Stores ({len(stores)})")
        
        for store in stores:
            with st.expander(f"🏪 {store['name']} - {store['location']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Status:** {format_status_badge(store['status'])}", unsafe_allow_html=True)
                    opening_date = datetime.fromisoformat(store['opening_date'].replace('Z', '+00:00'))
                    st.write(f"**📅 Opening Date:** {opening_date.strftime('%Y-%m-%d')}")
                
                with col2:
                    # Get store details
                    store_details = get_api_data(f"/stores/{store['id']}")
                    if store_details:
                        st.write(f"**👥 Team Members:** {store_details.get('team_members_count', 0)}")
                        st.write(f"**📝 Total Tasks:** {store_details.get('total_tasks', 0)}")
                
                with col3:
                    if store_details:
                        completion = store_details.get('completion_percentage', 0)
                        st.write(f"**✅ Completion:** {completion:.1f}%")
                        st.progress(completion / 100)
                
                # View details button
                if st.button(f"👁️ View Details", key=f"view_{store['id']}", use_container_width=True):
                    st.session_state.selected_store = store['id']
                    st.rerun()
    else:
        st.info("ℹ️ No stores found. Create your first store to get started!")

elif page == "team":
    st.markdown('<div class="page-title">👥 Team Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Manage team members across all stores</div>', unsafe_allow_html=True)
    
    # Store selector
    stores = get_api_data("/stores")
    if stores:
        col1, col2 = st.columns([2, 3])
        with col1:
            store_options = {s['name']: s['id'] for s in stores}
            selected_store_name = st.selectbox("🔍 Filter by Store", ["All Stores"] + list(store_options.keys()))
        
        # Fetch team members
        with st.spinner("Loading team members..."):
            if selected_store_name == "All Stores":
                team_members = get_api_data("/team")
            else:
                store_id = store_options[selected_store_name]
                team_members = get_api_data(f"/team?store_id={store_id}")
        
        if team_members:
            st.markdown(f"### 👥 Team Members ({len(team_members)})")
            
            # Display as enhanced table
            df_team = pd.DataFrame(team_members)
            st.dataframe(
                df_team[['name', 'role', 'phone', 'email', 'is_active']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("ℹ️ No team members found")

elif page == "tasks":
    st.markdown('<div class="page-title">✅ Tasks & Checklists</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Track and manage all tasks across stores</div>', unsafe_allow_html=True)
    
    # Store selector
    stores = get_api_data("/stores")
    if stores:
        col1, col2 = st.columns([2, 3])
        with col1:
            store_options = {s['name']: s['id'] for s in stores}
            selected_store_name = st.selectbox("🔍 Select Store", list(store_options.keys()))
            store_id = store_options[selected_store_name]
        
        # Get checklists for store
        with st.spinner("Loading checklists..."):
            checklists = get_api_data(f"/checklists?store_id={store_id}")
        
        if checklists:
            for checklist in checklists:
                with st.expander(f"📋 {checklist['name']} ({checklist.get('category', 'general')})", expanded=True):
                    tasks = checklist.get('tasks', [])
                    
                    if tasks:
                        for task in tasks:
                            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                            
                            with col1:
                                # Task title with checkbox
                                completed = task['status'] == 'completed'
                                if st.checkbox(task['title'], value=completed, key=f"task_{task['id']}"):
                                    if not completed:
                                        # Update task status
                                        put_api_data(f"/checklists/tasks/{task['id']}", {'status': 'completed'})
                                        st.success(f"✅ Task '{task['title']}' marked as completed!")
                                        st.rerun()
                            
                            with col2:
                                priority_icons = {
                                    'low': '🟢 Low',
                                    'medium': '🟡 Medium',
                                    'high': '🟠 High',
                                    'critical': '🔴 Critical'
                                }
                                st.markdown(f"{priority_icons.get(task['priority'], '⚪ Unknown')}")
                            
                            with col3:
                                if task.get('due_date'):
                                    due_date = datetime.fromisoformat(task['due_date'].replace('Z', '+00:00'))
                                    st.write(f"📅 {due_date.strftime('%Y-%m-%d')}")
                            
                            with col4:
                                status_icons = {
                                    'pending': '⏳',
                                    'in_progress': '🔄',
                                    'completed': '✅',
                                    'blocked': '🚫'
                                }
                                st.markdown(f"{status_icons.get(task['status'], '⚪')}")
                    else:
                        st.info("ℹ️ No tasks in this checklist")
        else:
            st.info("ℹ️ No checklists found for this store")

elif page == "whatsapp":
    st.markdown('<div class="page-title">💬 Communications</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Manage WhatsApp groups and team communications</div>', unsafe_allow_html=True)
    
    with st.spinner("Loading communication groups..."):
        groups = get_api_data("/whatsapp/groups")
    
    if groups:
        st.markdown(f"### 💬 WhatsApp Groups ({len(groups)})")
        
        for group in groups:
            store = get_api_data(f"/stores/{group['store_id']}")
            
            with st.expander(f"💬 {group['group_name']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**🏪 Store:** {store['name'] if store else 'Unknown'}")
                    status_text = "✅ Active" if group['is_active'] else "📁 Archived"
                    st.write(f"**Status:** {status_text}")
                
                with col2:
                    created = datetime.fromisoformat(group['created_at'].replace('Z', '+00:00'))
                    st.write(f"**📅 Created:** {created.strftime('%Y-%m-%d')}")
                    if group.get('archived_at'):
                        archived = datetime.fromisoformat(group['archived_at'].replace('Z', '+00:00'))
                        st.write(f"**📁 Archived:** {archived.strftime('%Y-%m-%d')}")
                
                # Send message form
                if group['is_active']:
                    with st.form(f"send_message_{group['id']}"):
                        st.markdown("#### 📤 Send Message")
                        message = st.text_area("Message", placeholder="Type your message here...")
                        if st.form_submit_button("📨 Send Message", use_container_width=True):
                            if message:
                                result = post_api_data(f"/whatsapp/groups/{group['id']}/send", {'message': message})
                                if result:
                                    st.success(f"✅ Message sent to {result.get('sent_to', 0)} members")
                            else:
                                st.warning("⚠️ Please enter a message")
                
                # View archived conversations
                if not group['is_active']:
                    if st.button(f"👁️ View Archived Conversations", key=f"archive_{group['id']}", use_container_width=True):
                        archive_data = get_api_data(f"/whatsapp/groups/{group['id']}/archive")
                        if archive_data:
                            conversations = archive_data.get('conversations', [])
                            st.write(f"**📊 Total Messages:** {len(conversations)}")
                            for conv in conversations[:10]:  # Show first 10
                                timestamp = datetime.fromisoformat(conv['timestamp'].replace('Z', '+00:00'))
                                st.text(f"[{timestamp.strftime('%Y-%m-%d %H:%M')}] {conv['sender']}: {conv['message']}")
    else:
        st.info("ℹ️ No WhatsApp groups found")

elif page == "analytics":
    st.markdown('<div class="page-title">📊 Analytics & Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Comprehensive analytics and reporting</div>', unsafe_allow_html=True)
    
    # Report type selector
    col1, col2 = st.columns([2, 3])
    with col1:
        report_type = st.selectbox("📈 Select Report Type", ["Dashboard Overview", "Store Progress", "Task Analysis"])
    
    if report_type == "Dashboard Overview":
        with st.spinner("Loading analytics..."):
            dashboard_data = get_api_data("/analytics/dashboard")
        
        if dashboard_data:
            summary = dashboard_data.get('summary', {})
            
            # Enhanced metrics display
            st.markdown("### 📊 System Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📦 Total Stores", summary.get('total_stores', 0))
            with col2:
                st.metric("📝 Total Tasks", summary.get('total_tasks', 0))
            with col3:
                completion_rate = (summary.get('completed_tasks', 0) / max(summary.get('total_tasks', 1), 1)) * 100
                st.metric("✅ Completion Rate", f"{completion_rate:.1f}%")
            with col4:
                st.metric("⚠️ Overdue", summary.get('overdue_tasks', 0))
            
            # Visualizations
            st.markdown("---")
            stores = dashboard_data.get('stores', [])
            if stores:
                df_stores = pd.DataFrame(stores)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Status distribution
                    fig_status = px.pie(
                        df_stores,
                        names='status',
                        title='Store Status Distribution',
                        color_discrete_map={
                            'planning': '#fbbf24',
                            'in_progress': '#3b82f6',
                            'completed': '#10b981',
                            'delayed': '#ef4444'
                        }
                    )
                    fig_status.update_layout(font=dict(family="Inter, sans-serif"))
                    st.plotly_chart(fig_status, use_container_width=True)
                
                with col2:
                    # Completion progress
                    fig_progress = go.Figure(go.Bar(
                        x=df_stores['name'],
                        y=df_stores['completion_percentage'],
                        marker_color='#667eea',
                        text=df_stores['completion_percentage'].apply(lambda x: f"{x:.1f}%"),
                        textposition='outside'
                    ))
                    fig_progress.update_layout(
                        title='Store Completion Progress',
                        xaxis_title='Store',
                        yaxis_title='Completion %',
                        font=dict(family="Inter, sans-serif"),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_progress, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #64748b; font-size: 0.875rem;">
        <p style="margin: 0;">Store Opening AI Management System v3.0</p>
        <p style="margin: 0.25rem 0 0 0;">Built with ❤️ for efficient store opening management</p>
    </div>
""", unsafe_allow_html=True)
