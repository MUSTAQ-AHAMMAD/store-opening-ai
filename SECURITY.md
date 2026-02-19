# Security Policy

## Environment Variables

This application uses environment variables for sensitive configuration. 

### Setup Instructions

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your actual credentials:
   - Generate a secure `SECRET_KEY` using: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Add your Twilio Account SID and Auth Token from [Twilio Console](https://console.twilio.com/)
   - Configure your Twilio WhatsApp number

3. **Never commit `.env` to version control**

### Rotating Credentials

If credentials are exposed:
1. Immediately rotate Twilio Auth Token in Twilio Console
2. Generate new SECRET_KEY
3. Update `.env` file locally
4. Restart the application

## Reporting a Vulnerability

If you discover a security vulnerability, please email the repository owner directly.
