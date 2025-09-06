# Daily Affirmations API 💕

A beautiful API that generates personalized daily affirmations and sends them via email automatically. Perfect for sending loving messages to your significant other when you can't be there in person.

## Features ✨

- **AI-Powered Affirmations**: Uses OpenAI GPT-4 to generate authentic, personalized messages
- **Daily Email Automation**: Automatically sends beautiful HTML emails at scheduled times
- **Beautiful Email Design**: Stunning gradient backgrounds and modern styling
- **Web Interface**: Streamlit GUI for easy interaction
- **RESTful API**: Full API endpoints for integration
- **Flexible Scheduling**: Customizable send times
- **Error Handling**: Robust retry logic and error management

## Quick Start 🚀

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration (Gmail example)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
RECIPIENT_EMAIL=recipient_email@gmail.com

# Optional: Custom SMTP settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Streamlit secrets (for GUI)
AFFIRMATION_API_URL=http://localhost:8000
```

### 3. Gmail Setup (Recommended)

For Gmail, you'll need to:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password in `SENDER_PASSWORD`

### 4. Run the Application

#### Start the API Server
```bash
python main.py
```
Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Start the Web Interface
```bash
streamlit run gui.py
```

## API Endpoints 📡

### Core Endpoints

- `GET /` - Generate a random affirmation
- `POST /send-email` - Send an affirmation email immediately
- `POST /test-email` - Test email configuration

### Scheduler Endpoints

- `POST /start-scheduler?hour=9&minute=0` - Start daily scheduler (default: 9:00 AM)
- `POST /stop-scheduler` - Stop the daily scheduler
- `GET /scheduler-status` - Check scheduler status and next run time

### Example Usage

```bash
# Generate an affirmation
curl http://localhost:8000/

# Send an email immediately
curl -X POST http://localhost:8000/send-email

# Start daily scheduler at 8:30 AM
curl -X POST "http://localhost:8000/start-scheduler?hour=8&minute=30"

# Check scheduler status
curl http://localhost:8000/scheduler-status
```

## Email Providers Setup 📧

### Gmail (Recommended)
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SENDER_EMAIL=your_email@outlook.com
SENDER_PASSWORD=your_password
```

### Yahoo
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SENDER_EMAIL=your_email@yahoo.com
SENDER_PASSWORD=your_app_password
```

### Custom SMTP
```env
SMTP_SERVER=your_smtp_server.com
SMTP_PORT=587
SENDER_EMAIL=your_email@domain.com
SENDER_PASSWORD=your_password
```

## File Structure 📁

```
affirmations_api/
├── main.py              # FastAPI server with all endpoints
├── email_service.py     # Email sending functionality
├── scheduler.py         # Daily scheduling logic
├── gui.py              # Streamlit web interface
├── chat.py             # WebSocket chat functionality
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # This file
```

## Customization 🎨

### Change Email Send Time
```python
# In main.py, modify the startup event
scheduler.start_scheduler(hour=8, minute=30)  # 8:30 AM
```

### Customize Affirmation Style
Edit the system prompt in `main.py`:
```python
"content": (
    "You are [Your Name] — authentic, sharp, never corny. "
    "Your affirmations are deep, original, and well-worded..."
)
```

### Modify Email Design
Edit the HTML template in `email_service.py` in the `create_affirmation_email` method.

## Troubleshooting 🔧

### Common Issues

1. **Email not sending**:
   - Check your email credentials
   - Ensure 2FA is enabled and app password is used
   - Verify SMTP settings

2. **Scheduler not working**:
   - Check if the application is running continuously
   - Verify timezone settings
   - Check logs for errors

3. **OpenAI API errors**:
   - Verify your API key is correct
   - Check your OpenAI account balance
   - Ensure you have access to GPT-4

### Logs
The application logs all activities. Check the console output for detailed error messages.

## Security Notes 🔒

- Never commit your `.env` file to version control
- Use app passwords instead of your main email password
- Consider using environment variables in production
- Regularly rotate your API keys

## Production Deployment 🚀

For production deployment:

1. Use a process manager like PM2 or systemd
2. Set up proper logging
3. Use environment variables instead of .env files
4. Consider using a database to track sent emails
5. Set up monitoring and alerts

## License 📄

This project is for personal use. Feel free to modify and adapt it for your needs.

---

Made with ❤️ for sending love when you can't be there in person.
