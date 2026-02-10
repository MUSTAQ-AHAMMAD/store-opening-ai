# Deployment Guide

## Production Deployment Options

### Option 1: Deploy to Heroku

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Option 2: Deploy to AWS EC2

1. Launch Ubuntu EC2 instance
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql -y
```

3. Setup application and configure nginx

### Option 3: Docker Deployment

Use docker-compose for easy deployment:
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
  api:
    build: .
    ports:
      - "5000:5000"
```

See full deployment documentation for detailed steps.
