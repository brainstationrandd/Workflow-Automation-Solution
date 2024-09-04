from app.repository.job_repository import JobRepository
import requests
from app.config import MAILGUN_API_KEY, MAILGUN_DOMAIN
from utils.logger import logger
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def scheduled_task():
    expired_jobs = JobRepository.get_expired_jobs()
    logger.info(f"expired jobs: {expired_jobs}")

    if not expired_jobs: return

    emails = [JobRepository.get_email_by_job_id(job[0]) for job in expired_jobs]
    logger.info(f"emails: {emails}")

    for email in emails:
        send_email(email)


def send_email(recipient_email: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "abuu.darda.ad@gmail.com"
    smtp_password = "psam imii jyuc ozhp"  # Use the app-specific password here

    # Email content
    from_email = smtp_user
    to_email = recipient_email
    subject = "job end check fast"
    body = "ayo job application time over. check cv asap."


    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
# Convert the MIMEMultipart object to a string
    msg_string = msg.as_string()
    print(type(msg_string))

    # Send the email
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(smtp_user, smtp_password)  # Login to the email account

        # Send the email
        server.sendmail(from_email, to_email, msg_string)

        logger.info("Email sent successfully!")
    except Exception as e:
        logger.info(f"Failed to send email: {e}")
    finally:
        server.quit()  # Terminate the SMTP session