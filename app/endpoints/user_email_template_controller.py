from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.models.user_email_template import UserEmailTemplate  # Replace with actual import path
from app.db import get_db  # Replace with actual import path
from app.schema.user_email_template import UserEmailTemplateCreate, UserEmailTemplateUpdate  # Replace with actual import path
from utils.logger import logger

router = APIRouter()

@router.post("/user_email_templates/")
async def create_user_email_template(user_email_template: UserEmailTemplateCreate, db: Session = Depends(get_db)):
    try:
        db_user_email_template = UserEmailTemplate(**user_email_template.dict())
        db.add(db_user_email_template)
        db.commit()
        db.refresh(db_user_email_template)
        return db_user_email_template
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to create user email template")

@router.get("/user_email_templates/{user_id}")
async def get_user_email_template_by_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user_email_template = db.query(UserEmailTemplate).filter(UserEmailTemplate.user_id == user_id).first()
        if not user_email_template:
            # Create a default template if the user doesn't exist
            default_template = UserEmailTemplateCreate(
                user_id=user_id,
                screening_template=(
                    '<p>Dear Candidate,</p><p>We are pleased to inform you that you have been selected for a <strong>{status} Interview</strong> for the position of {job_title} at {company_name}.</p>'
                    '<p><strong>Date:</strong> {schedule}</p><p>Please be prepared to discuss your experience and qualifications.</p><p>Looking forward to speaking with you.</p>'
                    '<p>Best regards,<br>{company_name} Team</p>'
                ),
                technical_template=(
                    '<p>Dear Candidate,</p><p>Congratulations on advancing to the <strong>{status} Interview</strong> stage for the {job_title} position at {company_name}.</p>'
                    '<p><strong>Date:</strong> {schedule}</p><p>The interview will cover technical aspects relevant to the role, so please be prepared.</p>'
                    '<p>We look forward to assessing your technical skills.</p><p>Best regards,<br>{company_name} Team</p>'
                ),
                hr_template=(
                    '<p>Dear Candidate,</p><p>We are excited to invite you for the <strong>{status} Interview</strong> for the {job_title} position at {company_name}.</p>'
                    '<p><strong>Date:</strong> {schedule}</p><p>During the interview, we will discuss your background and fit for the role.</p><p>We are excited to get to know you better.</p>'
                    '<p>Best regards,<br>{company_name} Team</p>'
                ),
                final_template=(
                    '<p>Dear Candidate,</p><p>We are pleased to invite you to the <strong>{status} Interview</strong> for the {job_title} position at {company_name}.</p>'
                    '<p><strong>Date:</strong> {schedule}</p><p>This is the last step in our recruitment process, and we look forward to finalizing your candidacy.</p>'
                    '<p>Best regards,<br>{company_name} Team</p>'
                ),
                offered_template=(
                    '<p>Dear Candidate,</p><p>We are delighted to extend an <strong>Offer</strong> for the {job_title} position at {company_name}.</p>'
                    '<p><strong>Offer Details:</strong></p><ul><li><strong>Position:</strong> {job_title}</li><li><strong>Salary:</strong> [Salary Details]</li>'
                    '<li><strong>Benefits:</strong> [List Benefits]</li></ul><p>Please review the offer details and let us know if you have any questions.</p>'
                    '<p>We hope to have you as part of our team!</p><p>Best regards,<br>{company_name} Team</p>'
                ),
                rejected_template=(
                    '<p>Dear Candidate,</p><p>Thank you for your time and effort during the interview process for the {job_title} position at {company_name}.</p>'
                    '<p>After careful consideration, we regret to inform you that we will not be moving forward with your application at this time.</p>'
                    '<p>We appreciate your interest in {company_name} and encourage you to apply for future openings.</p>'
                    '<p>Best wishes for your job search.</p><p>Sincerely,<br>{company_name} Team</p>'
                ),
                accepted_template=(
                    '<p>Dear Candidate,</p><p>We are thrilled to hear that you have accepted our offer for the <strong>{job_title}</strong> position at {company_name}!</p>'
                    '<p><strong>We look forward to having you join the team on</strong> <strong>{schedule}</strong>.</p>'
                    '<p>Please let us know if you have any questions before your start date.</p><p>We are excited to welcome you aboard!</p>'
                    '<p>Best regards,<br>{company_name} Team</p>'
                )
            )
            db_user_email_template = UserEmailTemplate(**default_template.dict())
            db.add(db_user_email_template)
            db.commit()
            db.refresh(db_user_email_template)
            return db_user_email_template
        return user_email_template
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to fetch user email template")

@router.put("/user_email_templates/{user_id}")
async def update_user_email_template_status(user_id: int, user_email_template_update: UserEmailTemplateUpdate, db: Session = Depends(get_db)):
    try:
        db_user_email_template = db.query(UserEmailTemplate).filter(UserEmailTemplate.user_id == user_id).first()
        if not db_user_email_template:
            raise HTTPException(status_code=404, detail="User email template not found")
        
        for key, value in user_email_template_update.dict().items():
            if value is not None:
                setattr(db_user_email_template, key, value)
        
        db.commit()
        db.refresh(db_user_email_template)
        return db_user_email_template
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to update user email template status")