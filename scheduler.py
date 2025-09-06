import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import os
from email_service import EmailService
from openai import OpenAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AffirmationScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.email_service = EmailService()
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_affirmation(self) -> str:
        """Generate a daily affirmation using OpenAI."""
        try:
            response = self.openai_client.chat.completions.create(
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
                            "Avoid corny or generic phrasing; it should feel authentic, charming, and real."
                        ),
                    },
                ],
                max_tokens=50,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Failed to generate affirmation: {str(e)}")
            return "You are loved and appreciated more than words can express 💕"

    def send_daily_affirmation(self):
        """Generate and send the daily affirmation email."""
        try:
            logger.info("Starting daily affirmation email process...")

            # Generate affirmation
            affirmation = self.generate_affirmation()
            logger.info(f"Generated affirmation: {affirmation}")

            # Send email
            success = self.email_service.send_affirmation_email(affirmation)

            if success:
                logger.info("Daily affirmation email sent successfully!")
            else:
                logger.error("Failed to send daily affirmation email")

        except Exception as e:
            logger.error(f"Error in daily affirmation process: {str(e)}")

    def start_scheduler(self, hour: int = 7, minute: int = 0):
        """Start the daily email scheduler."""
        try:
            # Add the daily job
            self.scheduler.add_job(
                func=self.send_daily_affirmation,
                trigger=CronTrigger(hour=hour, minute=minute),
                id="daily_affirmation",
                name="Send Daily Affirmation Email",
                replace_existing=True,
            )

            # Start the scheduler
            self.scheduler.start()
            logger.info(
                f"Daily affirmation scheduler started. Emails will be sent at {hour:02d}:{minute:02d} daily."
            )

        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")

    def stop_scheduler(self):
        """Stop the scheduler."""
        try:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped.")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}")

    def test_email_now(self):
        """Send a test email immediately."""
        logger.info("Sending test affirmation email...")
        self.send_daily_affirmation()

    def get_next_run_time(self):
        """Get the next scheduled run time."""
        try:
            job = self.scheduler.get_job("daily_affirmation")
            if job:
                return job.next_run_time
            return None
        except Exception as e:
            logger.error(f"Error getting next run time: {str(e)}")
            return None
