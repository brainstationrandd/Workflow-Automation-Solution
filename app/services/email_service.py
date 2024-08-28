from app.repository.job_repository import JobRepository
import requests
from app.config import MAILGUN_API_KEY, MAILGUN_DOMAIN
from utils.logger import logger
def scheduled_task():
    expired_jobs = JobRepository.get_expired_jobs()
    logger.info(f"expired jobs: {expired_jobs}")

    if not expired_jobs: return

    emails = [JobRepository.get_email_by_job_id(job) for job in expired_jobs]
    logger.info(f"emails: {emails}")

    for email in emails:
        send_email(email)

def send_email(recipient_email: str):
    """Send an email to the recipient using Mailgun."""
    # MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    # MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    MAILGUN_BASE_URL = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    
    sender_email = f"Pro Rizzler <mailgun@{MAILGUN_DOMAIN}>"
    
    data = {
        "from": sender_email,
        "to": recipient_email,
        "subject": "Job End Notification",
        "text": "Hello,\n\nThis is a reminder that your job has ended.\n\nBest regards,\nYour Team",
        "html": """
            <html>
            <body>
                <h1>Job End Notification</h1>
                <p>This is a reminder that your job has ended.</p>
                <p>Best regards,</p>
                <p>Your Team</p>
            </body>
            </html>
        """
    }
    
    try:
        response = requests.post(
            MAILGUN_BASE_URL,
            auth=("api", MAILGUN_API_KEY),
            data=data
        )
        
        response.raise_for_status()
        print(f"Email sent to {recipient_email}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# def send_simple_message():
#   	return requests.post(
#   		"https://api.mailgun.net/v3/sandboxf2df3cff1a5b4eb38793b438b9ad3336.mailgun.org/messages",
#   		auth=("api", "f6f4de29ba4b975a0b310aba84abfcc4-777a617d-231fec93"),
#   		data={"from": "Excited User <mailgun@sandboxf2df3cff1a5b4eb38793b438b9ad3336.mailgun.org>",
#   			"to": ["bar@example.com", "YOU@sandboxf2df3cff1a5b4eb38793b438b9ad3336.mailgun.org"],
#   			"subject": "Hello",
#   			"text": "Testing some Mailgun awesomeness!"})
