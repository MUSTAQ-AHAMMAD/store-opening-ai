# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, no authentication is required for beta testing. In production, implement JWT or OAuth2.

## Store Endpoints

### List All Stores
```
GET /stores
```

### Get Store Details
```
GET /stores/<id>
```

### Create Store
```
POST /stores
Content-Type: application/json

{
  "name": "New Store Name",
  "location": "City, State",
  "opening_date": "2024-04-01T00:00:00",
  "status": "planning"
}
```

## Team Member Endpoints

### List Team Members
```
GET /team?store_id=<optional>
```

### Create Team Member
```
POST /team
Content-Type: application/json

{
  "name": "John Doe",
  "role": "Store Manager",
  "phone": "+15551234567",
  "email": "john.doe@company.com",
  "store_id": 1
}
```

## Task Endpoints

### List Tasks
```
GET /checklists/<checklist_id>/tasks
```

### Update Task
```
PUT /checklists/tasks/<id>
Content-Type: application/json

{
  "status": "completed"
}
```

## WhatsApp Endpoints

### Send Message to Group
```
POST /whatsapp/groups/<id>/send
Content-Type: application/json

{
  "message": "Hello team!"
}
```

## Analytics Endpoints

### Dashboard Analytics
```
GET /analytics/dashboard
```

### Store Progress
```
GET /analytics/store/<id>/progress
```
