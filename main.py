from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv
from email_service import EmailService
from scheduler import AffirmationScheduler

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
email_service = EmailService()
scheduler = AffirmationScheduler()

app = FastAPI(
    title="Daily Affirmations API",
    description="API for generating and sending daily affirmations",
)


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.get("/")
async def admin_dashboard():
    """Serve the admin dashboard."""
    return FileResponse("admin_dashboard.html")


@app.get("/health")
async def health():
    return {"message": "OK"}


@app.get("/get-affirmation")
async def get_affirmation():
    """Generate a daily affirmation."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are PB — authentic, sharp, never corny. "
                        "Your affirmations for your girlfriend are deep, original, and well-worded, "
                        "with richer vocabulary and poetic charm. "
                        "Avoid clichés, keep it personal, captivating, and real."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Generate one short message for my girlfriend — it can be an affirmation, compliment, reassurance, gratitude, flirty line, or poetic note. "
                        "Make it deep, original, vocabulary-rich, slightly poetic but natural. "
                        "Avoid corny or generic phrasing; it should feel authentic, charming, and real, and saying 'in the quiet tapestry of our lives'."
                    ),
                },
            ],
            max_tokens=50,
            temperature=0.7,
        )
        affirmation = response.choices[0].message.content.strip()
        return {"affirmation": affirmation}
    except Exception as e:
        logger.error(f"Error generating affirmation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate affirmation")


@app.post("/send-email")
async def send_affirmation_email():
    """Send a daily affirmation email immediately."""
    try:
        # Generate affirmation
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are PB — authentic, sharp, never corny. "
                        "Your affirmations for your girlfriend are deep, original, and well-worded, "
                        "with richer vocabulary and poetic charm. "
                        "Avoid clichés, keep it personal, captivating, and real."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Generate one short message for my girlfriend — it can be an affirmation, compliment, reassurance, gratitude, flirty line, or poetic note. "
                        "Make it deep, original, vocabulary-rich, slightly poetic but natural. "
                        "Avoid corny or generic phrasing; it should feel authentic, charming, and real, and saying 'in the quiet tapestry..'."
                    ),
                },
            ],
            max_tokens=50,
            temperature=0.7,
        )
        affirmation = response.choices[0].message.content.strip()

        # Send email
        success = email_service.send_affirmation_email(affirmation)

        if success:
            return {"message": "Email sent successfully", "affirmation": affirmation}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send email")


@app.post("/start-scheduler")
async def start_daily_scheduler(hour: int = 9, minute: int = 0):
    """Start the daily email scheduler."""
    try:
        scheduler.start_scheduler(hour, minute)
        next_run = scheduler.get_next_run_time()
        return {
            "message": f"Daily scheduler started. Emails will be sent at {hour:02d}:{minute:02d} daily.",
            "next_run_time": next_run.isoformat() if next_run else None,
        }
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start scheduler")


@app.post("/stop-scheduler")
async def stop_daily_scheduler():
    """Stop the daily email scheduler."""
    try:
        scheduler.stop_scheduler()
        return {"message": "Daily scheduler stopped"}
    except Exception as e:
        logger.error(f"Error stopping scheduler: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to stop scheduler")


@app.get("/scheduler-status")
async def get_scheduler_status():
    """Get the current status of the scheduler."""
    try:
        next_run = scheduler.get_next_run_time()
        return {
            "scheduler_running": scheduler.scheduler.running,
            "next_run_time": next_run.isoformat() if next_run else None,
        }
    except Exception as e:
        logger.error(f"Error getting scheduler status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get scheduler status")


@app.post("/test-email")
async def test_email_connection():
    """Test the email configuration and send a test email."""
    try:
        # Test connection
        connection_ok = email_service.test_email_connection()
        if not connection_ok:
            raise HTTPException(status_code=500, detail="Email connection test failed")

        # Send test email
        scheduler.test_email_now()
        return {"message": "Test email sent successfully"}
    except Exception as e:
        logger.error(f"Error testing email: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to test email")


@app.on_event("startup")
async def startup_event():
    """Start the scheduler when the application starts."""
    try:
        # Check if email is configured
        if all(
            [
                os.getenv("SENDER_EMAIL"),
                os.getenv("SENDER_PASSWORD"),
                os.getenv("RECIPIENT_EMAIL"),
            ]
        ):
            # Start scheduler with default time (9:00 AM)
            scheduler.start_scheduler()
            logger.info("Application started with daily email scheduler enabled")
        else:
            logger.warning(
                "Email not configured. Scheduler will not start automatically."
            )
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop the scheduler when the application shuts down."""
    try:
        scheduler.stop_scheduler()
        logger.info("Application shutdown - scheduler stopped")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")
