"""
Store Opening AI Management System - Dashboard
Streamlit-based web interface for managing store openings
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Configure page
st.set_page_config(
    page_title="Store Opening AI Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:5000/api"

# Custom CSS
st.markdown("""
    <style>
    /* Import Google Fonts and Font Awesome */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
    
    * {
        font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .status-planning { background-color: #ffd700; color: #000; }
    .status-in-progress { background-color: #4169e1; color: #fff; }
    .status-completed { background-color: #228b22; color: #fff; }
    .status-delayed { background-color: #dc143c; color: #fff; }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def get_api_data(endpoint):
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def post_api_data(endpoint, data):
    """Post data to API"""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def put_api_data(endpoint, data):
    """Update data via API"""
    try:
        response = requests.put(f"{API_BASE_URL}{endpoint}", json=data)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def format_status_badge(status):
    """Format status as HTML badge"""
    return f'<span class="status-badge status-{status}">{status.upper()}</span>'

# Sidebar navigation
st.sidebar.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=Store+Opening+AI", use_column_width=True)
st.sidebar.title("Navigation")

pages = {
    "<i class='fas fa-home'></i> Dashboard": "dashboard",
    "<i class='fas fa-store'></i> Stores": "stores",
    "<i class='fas fa-users'></i> Team Members": "team",
    "<i class='fas fa-tasks'></i> Checklists & Tasks": "tasks",
    "<i class='fab fa-whatsapp'></i> WhatsApp Groups": "whatsapp",
    "<i class='fas fa-chart-line'></i> Analytics": "analytics"
}

selected_page = st.sidebar.radio("Go to", list(pages.keys()))
page = pages[selected_page]

# Main content
if page == "dashboard":
    st.markdown('<div class="main-header"><i class="fas fa-store-alt"></i> Store Opening Dashboard</div>', unsafe_allow_html=True)
    
    # Fetch dashboard data
    dashboard_data = get_api_data("/analytics/dashboard")
    
    if dashboard_data:
        summary = dashboard_data.get('summary', {})
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Stores", summary.get('total_stores', 0))
            st.metric("Active Stores", summary.get('active_stores', 0))
        
        with col2:
            st.metric("Total Tasks", summary.get('total_tasks', 0))
            st.metric("Completed Tasks", summary.get('completed_tasks', 0))
        
        with col3:
            st.metric("Pending Tasks", summary.get('pending_tasks', 0))
            st.metric("Overdue Tasks", summary.get('overdue_tasks', 0), delta_color="inverse")
        
        with col4:
            st.metric("High Priority", summary.get('high_priority_tasks', 0))
            st.metric("Critical Priority", summary.get('critical_priority_tasks', 0), delta_color="inverse")
        
        # Upcoming openings
        st.subheader("📅 Upcoming Openings (Next 30 Days)")
        upcoming = dashboard_data.get('upcoming_openings', [])
        
        if upcoming:
            for opening in upcoming:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.write(f"**{opening['name']}**")
                with col2:
                    st.write(opening['location'])
                with col3:
                    opening_date = datetime.fromisoformat(opening['opening_date'].replace('Z', '+00:00'))
                    st.write(opening_date.strftime('%Y-%m-%d'))
                with col4:
                    days = opening.get('days_until_opening', 0)
                    st.write(f"{days} days")
        else:
            st.info("No upcoming openings in the next 30 days")
        
        # Store progress overview
        st.subheader("📊 Store Progress Overview")
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
                    'planning': '#ffd700',
                    'in_progress': '#4169e1',
                    'completed': '#228b22',
                    'delayed': '#dc143c'
                }
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Store details table
            st.dataframe(
                df_stores[['name', 'status', 'total_tasks', 'completed_tasks', 'completion_percentage']],
                use_container_width=True
            )

elif page == "stores":
    st.markdown('<div class="main-header"><i class="fas fa-store"></i> Store Management</div>', unsafe_allow_html=True)
    
    # Add new store button
    if st.button("➕ Add New Store"):
        st.session_state.show_add_store = True
    
    # Add store form
    if st.session_state.get('show_add_store', False):
        with st.form("add_store_form"):
            st.subheader("Add New Store")
            name = st.text_input("Store Name")
            location = st.text_input("Location")
            opening_date = st.date_input("Opening Date", min_value=datetime.now().date())
            status = st.selectbox("Status", ["planning", "in_progress", "completed", "delayed"])
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Create Store")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted and name and location:
                data = {
                    'name': name,
                    'location': location,
                    'opening_date': opening_date.isoformat(),
                    'status': status
                }
                result = post_api_data("/stores", data)
                if result:
                    st.success(f"Store '{name}' created successfully!")
                    st.session_state.show_add_store = False
                    st.rerun()
            
            if cancelled:
                st.session_state.show_add_store = False
                st.rerun()
    
    # Display stores
    stores = get_api_data("/stores")
    
    if stores:
        for store in stores:
            with st.expander(f"🏪 {store['name']} - {store['location']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Status:**", store['status'])
                    opening_date = datetime.fromisoformat(store['opening_date'].replace('Z', '+00:00'))
                    st.write("**Opening Date:**", opening_date.strftime('%Y-%m-%d'))
                
                with col2:
                    # Get store details
                    store_details = get_api_data(f"/stores/{store['id']}")
                    if store_details:
                        st.write("**Team Members:**", store_details.get('team_members_count', 0))
                        st.write("**Total Tasks:**", store_details.get('total_tasks', 0))
                
                with col3:
                    if store_details:
                        completion = store_details.get('completion_percentage', 0)
                        st.write("**Completion:**", f"{completion:.1f}%")
                        st.progress(completion / 100)
                
                # View details button
                if st.button(f"View Details", key=f"view_{store['id']}"):
                    st.session_state.selected_store = store['id']
                    st.rerun()

elif page == "team":
    st.markdown('<div class="main-header"><i class="fas fa-users"></i> Team Management</div>', unsafe_allow_html=True)
    
    # Store selector
    stores = get_api_data("/stores")
    if stores:
        store_options = {s['name']: s['id'] for s in stores}
        selected_store_name = st.selectbox("Filter by Store", ["All Stores"] + list(store_options.keys()))
        
        # Fetch team members
        if selected_store_name == "All Stores":
            team_members = get_api_data("/team")
        else:
            store_id = store_options[selected_store_name]
            team_members = get_api_data(f"/team?store_id={store_id}")
        
        if team_members:
            # Display as table
            df_team = pd.DataFrame(team_members)
            st.dataframe(
                df_team[['name', 'role', 'phone', 'email', 'is_active']],
                use_container_width=True
            )
        else:
            st.info("No team members found")

elif page == "tasks":
    st.markdown('<div class="main-header"><i class="fas fa-tasks"></i> Tasks & Checklists</div>', unsafe_allow_html=True)
    
    # Store selector
    stores = get_api_data("/stores")
    if stores:
        store_options = {s['name']: s['id'] for s in stores}
        selected_store_name = st.selectbox("Select Store", list(store_options.keys()))
        store_id = store_options[selected_store_name]
        
        # Get checklists for store
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
                                        st.rerun()
                            
                            with col2:
                                priority_colors = {
                                    'low': '<i class="fas fa-arrow-down" style="color: #22c55e;"></i>',
                                    'medium': '<i class="fas fa-minus" style="color: #eab308;"></i>',
                                    'high': '<i class="fas fa-arrow-up" style="color: #f97316;"></i>',
                                    'critical': '<i class="fas fa-exclamation-triangle" style="color: #ef4444;"></i>'
                                }
                                st.markdown(f"{priority_colors.get(task['priority'], '<i class=\"far fa-circle\"></i>')} {task['priority']}", unsafe_allow_html=True)
                            
                            with col3:
                                if task.get('due_date'):
                                    due_date = datetime.fromisoformat(task['due_date'].replace('Z', '+00:00'))
                                    st.write(due_date.strftime('%Y-%m-%d'))
                            
                            with col4:
                                status_colors = {
                                    'pending': '<i class="far fa-clock" style="color: #6b7280;"></i>',
                                    'in_progress': '<i class="fas fa-spinner" style="color: #3b82f6;"></i>',
                                    'completed': '<i class="fas fa-check-circle" style="color: #22c55e;"></i>',
                                    'blocked': '<i class="fas fa-ban" style="color: #ef4444;"></i>'
                                }
                                st.markdown(f"{status_colors.get(task['status'], '<i class=\"far fa-circle\"></i>')} {task['status']}", unsafe_allow_html=True)
                    else:
                        st.info("No tasks in this checklist")
        else:
            st.info("No checklists found for this store")

elif page == "whatsapp":
    st.markdown('<div class="main-header"><i class="fab fa-whatsapp"></i> WhatsApp Groups</div>', unsafe_allow_html=True)
    
    groups = get_api_data("/whatsapp/groups")
    
    if groups:
        for group in groups:
            store = get_api_data(f"/stores/{group['store_id']}")
            
            with st.expander(f"💬 {group['group_name']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Store:**", store['name'] if store else 'Unknown')
                    st.write("**Status:**", "Active" if group['is_active'] else "Archived")
                
                with col2:
                    created = datetime.fromisoformat(group['created_at'].replace('Z', '+00:00'))
                    st.write("**Created:**", created.strftime('%Y-%m-%d'))
                    if group.get('archived_at'):
                        archived = datetime.fromisoformat(group['archived_at'].replace('Z', '+00:00'))
                        st.write("**Archived:**", archived.strftime('%Y-%m-%d'))
                
                # Send message form
                if group['is_active']:
                    with st.form(f"send_message_{group['id']}"):
                        message = st.text_area("Send Message to Group")
                        if st.form_submit_button("Send"):
                            result = post_api_data(f"/whatsapp/groups/{group['id']}/send", {'message': message})
                            if result:
                                st.success(f"Message sent to {result.get('sent_to', 0)} members")
                
                # View archived conversations
                if not group['is_active']:
                    if st.button(f"View Archived Conversations", key=f"archive_{group['id']}"):
                        archive_data = get_api_data(f"/whatsapp/groups/{group['id']}/archive")
                        if archive_data:
                            conversations = archive_data.get('conversations', [])
                            st.write(f"**Total Messages:** {len(conversations)}")
                            for conv in conversations[:10]:  # Show first 10
                                timestamp = datetime.fromisoformat(conv['timestamp'].replace('Z', '+00:00'))
                                st.text(f"[{timestamp.strftime('%Y-%m-%d %H:%M')}] {conv['sender']}: {conv['message']}")
    else:
        st.info("No WhatsApp groups found")

elif page == "analytics":
    st.markdown('<div class="main-header"><i class="fas fa-chart-line"></i> Analytics & Reports</div>', unsafe_allow_html=True)
    
    # Report type selector
    report_type = st.selectbox("Select Report Type", ["Dashboard Overview", "Store Progress", "Task Analysis"])
    
    if report_type == "Dashboard Overview":
        dashboard_data = get_api_data("/analytics/dashboard")
        
        if dashboard_data:
            summary = dashboard_data.get('summary', {})
            
            # Create pie charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Store status distribution
                store_status = {
                    'Active': summary.get('active_stores', 0),
                    'Completed': summary.get('completed_stores', 0)
                }
                fig1 = px.pie(
                    values=list(store_status.values()),
                    names=list(store_status.keys()),
                    title='Store Status Distribution'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Task status distribution
                task_status = {
                    'Completed': summary.get('completed_tasks', 0),
                    'Pending': summary.get('pending_tasks', 0),
                    'Overdue': summary.get('overdue_tasks', 0)
                }
                fig2 = px.pie(
                    values=list(task_status.values()),
                    names=list(task_status.keys()),
                    title='Task Status Distribution',
                    color_discrete_sequence=['#228b22', '#ffd700', '#dc143c']
                )
                st.plotly_chart(fig2, use_container_width=True)
    
    elif report_type == "Store Progress":
        stores = get_api_data("/stores")
        
        if stores:
            store_options = {s['name']: s['id'] for s in stores}
            selected_store = st.selectbox("Select Store", list(store_options.keys()))
            store_id = store_options[selected_store]
            
            progress_data = get_api_data(f"/analytics/store/{store_id}/progress")
            
            if progress_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Tasks by status
                    tasks_by_status = progress_data.get('tasks_by_status', {})
                    fig1 = px.bar(
                        x=list(tasks_by_status.keys()),
                        y=list(tasks_by_status.values()),
                        title='Tasks by Status',
                        labels={'x': 'Status', 'y': 'Count'}
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Tasks by priority
                    tasks_by_priority = progress_data.get('tasks_by_priority', {})
                    fig2 = px.bar(
                        x=list(tasks_by_priority.keys()),
                        y=list(tasks_by_priority.values()),
                        title='Tasks by Priority',
                        labels={'x': 'Priority', 'y': 'Count'},
                        color=list(tasks_by_priority.keys()),
                        color_discrete_map={
                            'low': '#228b22',
                            'medium': '#ffd700',
                            'high': '#ff8c00',
                            'critical': '#dc143c'
                        }
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Daily progress
                daily_progress = progress_data.get('daily_progress', [])
                if daily_progress:
                    df_daily = pd.DataFrame(daily_progress)
                    fig3 = px.line(
                        df_daily,
                        x='date',
                        y='completed_tasks',
                        title='Daily Task Completion (Last 7 Days)',
                        labels={'completed_tasks': 'Tasks Completed', 'date': 'Date'}
                    )
                    st.plotly_chart(fig3, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**Store Opening AI**  
Version 1.0.0 (Beta)  
© 2024 Store Management System
""")
