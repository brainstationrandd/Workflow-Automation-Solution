from fastapi import FastAPI, HTTPException, APIRouter,Depends
from typing import List
from sqlalchemy.orm import Session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.models.job import Job  # Import the Job model
from app.db import get_db  
from pydantic import BaseModel
router = APIRouter()

# Define the request body using Pydantic
class EmailRequest(BaseModel):
    sender_email: str
    receiver_emails: List[str]
    job_id: int

def send_email(sender_email: str, receiver_email: str, position: str):
    try:
        # SMTP Server Setup
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_password = "rjsi snse kces tukw"  # Replace with the actual sender email password

        # Email Content
        subject = "Your Application Has Been Received"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
            <p>Dear Candidate,</p>
            <p>Thank you for your interest in the <strong>{position}</strong> position at our company.</p>
            <p>We are currently reviewing your application, and our HR team will contact you if we decide to move forward with your profile.</p>
            <p>Stay tuned for further updates!</p>
            <p style="margin-top: 20px;">Regards,<br>HR Team</p>
        </body>
        </html>
        """

        # Create the Email
        message = MIMEMultipart("alternative")
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        # Connect to the Server and Send Email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def send_email_1(sender_email: str, receiver_email: str, position: str):
    try:
        # SMTP Server Setup
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_password = "rjsi snse kces tukw"  # Replace with the actual sender email password

        # Email Content
        subject = "Your Application Has Been Received"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
            <p>Dear Candidate,</p>
            <p>Thank you for your interest in the <strong>{position}</strong> position at our company.</p>
            <p>You're selected for the next round. We will communicate with you soon.</p>
            <p style="margin-top: 20px;">Regards,<br>HR Team</p>
        </body>
        </html>
        """

        # Create the Email
        message = MIMEMultipart("alternative")
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        # Connect to the Server and Send Email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@router.post("/send-email/")
def email_endpoint(sender_email: str, receiver_email: str, position: str):
    send_email(sender_email, receiver_email, position)
    return {"message": "Email sent successfully!"}

@router.post("/send_multiple_emails/")
def send_multiple_emails_endpoint(request: EmailRequest, db: Session = Depends(get_db)):
    # Fetch job details from the database
    jobs = db.query(Job).filter(Job.id == request.job_id).first()
    if not jobs:
        return {"error": "Job not found"}

    position = jobs.name
    
    # Send emails to each receiver
    for receiver_email in request.receiver_emails:
        send_email_1(request.sender_email, receiver_email, position)
        
    return {"message": "Emails sent successfully!"}