from fastapi import FastAPI, HTTPException,APIRouter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

# def send_email(sender_email: str, receiver_email: str, position: str):
#     try:
#         # SMTP Server Setup
#         smtp_server = "smtp.gmail.com"
#         smtp_port = 587
#         sender_password = "rjsi snse kces tukw"  # Replace with the actual sender email password

#         # Email Content
#         subject = "Your Application Has Been Received"
#         body = f"""
#         Dear Candidate,

#         Thank you for your interest in the {position} position at our company.
#         We are currently reviewing your application, and our HR team will contact you if we decide to move forward with your profile.

#         Stay tuned for further updates!

#         Regards,
#         HR Team
#         """

#         # Create the Email
#         message = MIMEMultipart()
#         message["From"] = sender_email
#         message["To"] = receiver_email
#         message["Subject"] = subject
#         message.attach(MIMEText(body, "plain"))

#         # Connect to the Server and Send Email
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()  # Upgrade the connection to secure
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, receiver_email, message.as_string())

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


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
    
@router.post("/send-email/")
def email_endpoint(sender_email: str, receiver_email: str, position: str):
    send_email(sender_email, receiver_email, position)
    return {"message": "Email sent successfully!"}
