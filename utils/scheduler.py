from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time


# Initialize the scheduler
scheduler = BackgroundScheduler()

# Add the job with a cron trigger
scheduler.add_job(scheduled_task, CronTrigger(hour=14, minute=0))  # Run every day at 14:00 (2:00 PM)

