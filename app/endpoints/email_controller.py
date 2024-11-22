from fastapi import FastAPI, HTTPException, APIRouter,Depends
from typing import List
from sqlalchemy.orm import Session
import smtplib
from pytz import timezone, utc 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.models.job import Job  # Import the Job model
from app.db import get_db  
from pydantic import BaseModel
from app.endpoints.interview_progress_controller import stage_update,append_note_by_appication_uuid
from uuid import UUID
from datetime import datetime
router = APIRouter()

# Define the request body using Pydantic
class EmailRequest(BaseModel):
    sender_email: str
    receiver_emails: List[str]
    job_id: int

def send_email(receiver_email: str, position: str,company_name:str,email_content:str):
    try:
        # SMTP Server Setup
        sender_email ="nabibpallab22@gmail.com"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_password = "rjsi snse kces tukw"  # Replace with the actual sender email password

        # Email Content
        subject = " Interview Process Update for the position of "+position+" at "+company_name
        body = email_content

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
    
def send_email_1(sender_email: str, receiver_email: str,email_content:str):
    try:
        # SMTP Server Setup
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_password = "rjsi snse kces tukw"  # Replace with the actual sender email password

        # Email Content
        subject = "Your Application Has Been Received"
        body = email_content

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

class Email(BaseModel):
    candidate_email: str
    email_content: str
    job_title: str
    company_name: str
    stage: str
    candidate_id:UUID
    scheduled_date:str
    
# @router.post("/send-email/")
# def email_endpoint(request: Email, db: Session = Depends(get_db)):
#         try:
#             receiver_email = request.candidate_email
#             email_content = request.email_content
#             position = request.job_title
#             company_name = request.company_name
#             stage = request.stage
#             candidate_id = request.candidate_id
#             scheduled_date = request.scheduled_date

#             # Convert scheduled_date to human-readable format
#             scheduled_date_human_readable = datetime.strptime(scheduled_date, "%Y-%m-%dT%H:%M:%S").strftime("%B %d, %Y at %I:%M %p")

#             send_email(receiver_email, position, company_name, email_content)
#             stage_update(stage, candidate_id, db)

#             if stage in ['SCREENING', 'TECHNICAL', 'HR', 'FINAL', 'OFFERED']:
#                 append_note_by_appication_uuid(f"Application Moved to {stage} Scheduled at {scheduled_date_human_readable}", candidate_id, db)
#             elif stage == 'ACCEPTED':
#                 append_note_by_appication_uuid(f"Applicant has ACCEPTED to Join Scheduled at {scheduled_date_human_readable}", candidate_id, db)
#             elif stage == 'REJECTED':
#                 append_note_by_appication_uuid(f"Applicant has been REJECTED at {scheduled_date_human_readable}", candidate_id, db)

#             return {"message": f"Email sent successfully to {receiver_email}"}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-email/")
def email_endpoint(request: Email, db: Session = Depends(get_db)):
    try:
        # Extract values from the request
        receiver_email = request.candidate_email
        email_content = request.email_content
        position = request.job_title
        company_name = request.company_name
        stage = request.stage
        candidate_id = request.candidate_id
        scheduled_date = request.scheduled_date

        # Debug: Log received scheduled_date
        print("Received scheduled_date (UTC):", scheduled_date)

        # Parse the received ISO date as UTC
        try:
            scheduled_date_obj = datetime.strptime(scheduled_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            scheduled_date_obj = utc.localize(scheduled_date_obj)  # Ensure it is treated as UTC
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date format for scheduled_date: {scheduled_date}. Expected ISO 8601 UTC format."
            )

        # Convert UTC to local timezone (e.g., 'America/New_York')
        local_tz = timezone('Asia/Dhaka')  # Replace with your desired timezone
        scheduled_date_local = scheduled_date_obj.astimezone(local_tz)

        # Convert to human-readable format
        scheduled_date_human_readable = scheduled_date_local.strftime("%B %d, %Y at %I:%M %p")
        print("Parsed scheduled_date (local):", scheduled_date_human_readable)

        # Send the email
        send_email(receiver_email, position, company_name, email_content)
        print("scheduled_date_local:", scheduled_date_local)
        # Update the stage
        stage_update(stage, candidate_id,scheduled_date_local , db)

        # Append notes based on the stage
        stage_note_mapping = {
            'SCREENING': f"Application Moved to SCREENING Scheduled at {scheduled_date_human_readable}",
            'TECHNICAL': f"Application Moved to TECHNICAL Scheduled at {scheduled_date_human_readable}",
            'HR': f"Application Moved to HR Scheduled at {scheduled_date_human_readable}",
            'FINAL': f"Application Moved to FINAL Scheduled at {scheduled_date_human_readable}",
            'OFFERED': f"Application Moved to OFFERED Scheduled at {scheduled_date_human_readable}",
            'ACCEPTED': f"Applicant has ACCEPTED to Join Scheduled at {scheduled_date_human_readable}",
            'REJECTED': f"Applicant has been REJECTED at {scheduled_date_human_readable}"
        }

        note_message = stage_note_mapping.get(stage, "")
        if note_message:
            append_note_by_appication_uuid(note_message, candidate_id, db)

        return {"message": f"Email sent successfully to {receiver_email}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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