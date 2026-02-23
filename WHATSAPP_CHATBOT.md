# WhatsApp AI Chatbot – Setup & Usage Guide

This guide explains how the WhatsApp AI chatbot works, how to configure Twilio, and how team members interact with it.

---

## Overview

The Store Opening AI application includes a WhatsApp chatbot that:

- **Sends automatic follow-up reminders** to team members about overdue tasks and upcoming deadlines.
- **Broadcasts workflow stage notifications** (stage started, stage completed, opening date changes) to the whole team.
- **Responds intelligently** to incoming messages from team members using OpenAI GPT (or built-in fallback commands when OpenAI is unavailable).
- **Archives conversation history** for audit and review.

> **Note:** Twilio's API does not support programmatic creation of WhatsApp groups.  
> Instead, the system sends messages **individually** to each team member. From the team's perspective, this behaves just like a group broadcast — everyone receives the same update messages. Each member can also reply to the Twilio number to interact with the AI assistant privately.

---

## Architecture

```
Team Member (WhatsApp)
        │
        │  sends "status"
        ▼
Twilio WhatsApp Number
        │
        │  POST /api/whatsapp/webhook
        ▼
ChatbotService.handle_incoming_message()
        │
        ├─ Look up TeamMember by phone number
        ├─ Build context (pending tasks, store info, days until opening)
        ├─ AIService.generate_chatbot_response()   ← GPT-3.5 or fallback
        │
        ▼
WhatsAppService.send_message()
        │
        ▼
Team Member receives AI reply
```

---

## Configuration

### 1. Copy the example environment file

```bash
cp .env.example .env
```

### 2. Add your Twilio credentials to `.env`

```ini
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886   # Twilio sandbox or your approved number
TWILIO_PHONE_NUMBER=+14155238886

# Set to 'true' to test without sending real messages
TEST_MODE=false

# Optional: Enable AI-powered replies
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ **Never commit your `.env` file.** It is excluded by `.gitignore`.

### 3. Configure the Twilio Webhook

In the [Twilio Console](https://console.twilio.com/):

1. Go to **Messaging → Try it out → Send a WhatsApp message** (sandbox) or your **WhatsApp Sender** settings.
2. Under **"A Message Comes In"**, set the webhook URL to:
   ```
   https://<your-server>/api/whatsapp/webhook
   ```
   Method: **HTTP POST**
3. Save the configuration.

> For local development, use [ngrok](https://ngrok.com/) to expose your local server:
> ```bash
> ngrok http 5000
> # Twilio webhook URL becomes: https://<random>.ngrok.io/api/whatsapp/webhook
> ```

### 4. Join the Twilio Sandbox (trial accounts)

Each team member must send a one-time join message to the Twilio sandbox number **before** they can receive messages:

1. Open WhatsApp and send a message to the Twilio sandbox number.
2. The message content is the sandbox join code (e.g., `join loud-mountain`). Get yours from the [Twilio Console](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn).
3. Wait for the confirmation reply from Twilio.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and configure environment
cp .env.example .env
# Edit .env with your Twilio and OpenAI credentials

# 3. Start the backend
python app.py

# 4. (Local dev) Expose via ngrok and update Twilio webhook URL
ngrok http 5000

# 5. Verify configuration
curl http://localhost:5000/api/whatsapp/diagnostics
```

---

## API Endpoints

### `POST /api/whatsapp/webhook`
Twilio calls this endpoint when a team member sends a WhatsApp message.  
**Do not call this endpoint directly** — it is reserved for Twilio.

### `POST /api/whatsapp/groups`
Create a communication channel for a store. Automatically sends a welcome/onboarding message to all active team members.

```json
POST /api/whatsapp/groups
{
  "store_id": 1,
  "group_name": "Store XYZ - Opening Team"  // optional
}
```

Response includes `welcome_messages_sent` and `welcome_messages_failed` counts.

### `POST /api/whatsapp/groups/<group_id>/send`
Broadcast a manual message to all team members in a store group.

### `POST /api/whatsapp/send-follow-up`
Send a follow-up message to a specific phone number.

```json
{
  "phone": "+1234567890",
  "message": "Reminder: your task is due tomorrow"
}
```

### `GET /api/whatsapp/diagnostics`
Returns the current Twilio/chatbot configuration status without revealing credentials.

---

## Chatbot Commands

Team members send these text commands to the Twilio WhatsApp number:

| Command | What it does |
|---------|--------------|
| `hi` / `hello` / `help` | Show the welcome message and available commands |
| `status` | List your pending and in-progress tasks |
| `store` | Show store name, status, and days until opening |
| `done <task-id>` | Mark a task as completed (e.g., `done 42`) |
| *any other text* | AI-generated contextual reply (requires `OPENAI_API_KEY`) |

### Example Conversations

**Checking task status:**
```
Alice: status
Bot: 📋 Your pending tasks for *Store XYZ*:

• [HIGH] Install POS system – pending
• [MEDIUM] Configure network – in_progress
```

**Marking a task complete:**
```
Alice: done 42
Bot: ✅ Task *Install POS system* marked as completed!

Great work! Send *status* to see your remaining tasks.
```

**Asking about the store:**
```
Alice: store
Bot: 🏪 *Store XYZ*
Status: in_progress
Days until opening: 14
```

---

## Automated Notifications

In addition to chatbot replies, the system automatically sends WhatsApp messages to the team when:

- A new store communication channel is created (welcome message)
- A workflow stage is completed
- A new workflow stage begins
- The store opening date changes (timeline recalculated)
- A workflow stage is overdue (escalation messages)
- The store opening is complete (congratulations message)

These notifications are triggered by the **WorkflowService** and **APScheduler** and require no manual action.

---

## Testing

Run the chatbot tests with:

```bash
python -m pytest test_chatbot.py -v
```

To test without sending real WhatsApp messages, set `TEST_MODE=true` in `.env`.  
All messages will be logged to the console instead.

To verify your Twilio credentials:

```bash
python test_twilio_config.py
```

---

## Security Notes

- **Credentials**: Always store Twilio credentials in `.env`, never in code.
- **Webhook validation**: For production deployments, add Twilio request signature validation using `twilio.request_validator.RequestValidator` to ensure webhook calls originate from Twilio.
- **Phone number lookup**: The chatbot identifies users by their phone number. Ensure team members are registered with correct E.164-format phone numbers (e.g., `+14155238886`).
- **Sandbox restrictions**: Twilio trial accounts can only send messages to **verified** phone numbers. Upgrade to a paid account for unrestricted messaging.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Messages not delivered | Ensure recipient has joined the Twilio sandbox |
| `Twilio credentials not configured` log | Check `.env` has `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` |
| Webhook not called by Twilio | Verify webhook URL in Twilio Console; check ngrok is running |
| AI replies not working | Add `OPENAI_API_KEY` to `.env`; fallback commands still work |
| `TEST_MODE active` log | Set `TEST_MODE=false` in `.env` for real message delivery |

For more help, see:
- [QUICKSTART_TWILIO.md](./QUICKSTART_TWILIO.md) – Twilio sandbox setup
- [TEST_MODE_GUIDE.md](./TEST_MODE_GUIDE.md) – Testing without real messages
- [SECURITY.md](./SECURITY.md) – Credential management
