# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Seed beta testing data
python data/seed_beta_data.py
```

## Running the Application

### Option 1: Test Everything
```bash
python test_system.py
```

### Option 2: Start Services

**Terminal 1 - API Server:**
```bash
python app.py
```

**Terminal 2 - Dashboard:**
```bash
streamlit run frontend/dashboard.py
```

## Access

- **API**: http://localhost:5000/api
- **Dashboard**: http://localhost:8501

## Quick API Tests

```bash
# List all stores
curl http://localhost:5000/api/stores

# Get dashboard analytics
curl http://localhost:5000/api/analytics/dashboard

# List team members
curl http://localhost:5000/api/team
```

## Beta Testing Data

The system includes:
- 5 stores (various statuses)
- 24 team members
- 90 tasks across 20 checklists
- 5 WhatsApp groups
- 29 archived conversations
- 68 follow-up reminders

See full [README.md](README.md) for complete documentation.
