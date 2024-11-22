from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base  # Assuming Base is defined in the base module

class UserEmailTemplate(Base):
    __tablename__ = 'user_email_template'

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    screening_template = Column(Text, default=(
        '<p>Dear Candidate,</p><p>We are pleased to inform you that you have been selected for a <strong>{status} Interview</strong> for the position of {job_title} at {company_name}.</p>'
        '<p><strong>Date:</strong> {schedule}</p><p>Please be prepared to discuss your experience and qualifications.</p><p>Looking forward to speaking with you.</p>'
        '<p>Best regards,<br>{company_name} Team</p>'
    ))
    technical_template = Column(Text, default=(
        '<p>Dear Candidate,</p><p>Congratulations on advancing to the <strong>{status} Interview</strong> stage for the {job_title} position at {company_name}.</p>'
        '<p><strong>Date:</strong> {schedule}</p><p>The interview will cover technical aspects relevant to the role, so please be prepared.</p>'
        '<p>We look forward to assessing your technical skills.</p><p>Best regards,<br>{company_name} Team</p>'
    ))
    hr_template = Column(Text, default=(
        '<p>Dear Candidate,</p><p>We are excited to invite you for the <strong>{status} Interview</strong> for the {job_title} position at {company_name}.</p>'
        '<p><strong>Date:</strong> {schedule}</p><p>During the interview, we will discuss your background and fit for the role.</p><p>We are excited to get to know you better.</p>'
        '<p>Best regards,<br>{company_name} Team</p>'
    ))
    final_template = Column(Text, default=(
        '<p>Dear Candidate,</p><p>We are pleased to invite you to the <strong>{status} Interview</strong> for the {job_title} position at {company_name}.</p>'
        '<p><strong>Date:</strong> {schedule}</p><p>This is the last step in our recruitment process, and we look forward to finalizing your candidacy.</p>'
        '<p>Best regards,<br>{company_name} Team</p>'
    ))
    offered_template = Column(Text, default=(
        '<p>Dear Candidate,</p><p>We are delighted to extend an <strong>Offer</strong> for the {job_title} position at {company_name}.</p>'
        '<p><strong>Offer Details:</strong></p><ul><li><strong>Position:</strong> {job_title}</li><li><strong>Salary:</strong> [Salary Details]</li>'
        '<li><strong>Benefits:</strong> [List Benefits]</li></ul><p>Please review the offer details and let us know if you have any questions.</p>'
        '<p>We hope to have you as part of our team!</p><p>Best regards,<br>{company_name} Team</p>'
    ))
    rejected_template = Column(Text, default=(
        '<p>Dear Candidate,</p><p>Thank you for your time and effort during the interview process for the {job_title} position at {company_name}.</p>'
        '<p>After careful consideration, we regret to inform you that we will not be moving forward with your application at this time.</p>'
        '<p>We appreciate your interest in {company_name} and encourage you to apply for future openings.</p>'
        '<p>Best wishes for your job search.</p><p>Sincerely,<br>{company_name} Team</p>'
    ))
    accepted_template = Column(Text, default=(
        '<p>Dear Candidate,</p><p>We are thrilled to hear that you have accepted our offer for the <strong>{job_title}</strong> position at {company_name}!</p>'
        '<p><strong>We look forward to having you join the team on</strong> <strong>{schedule}</strong>.</p>'
        '<p>Please let us know if you have any questions before your start date.</p><p>We are excited to welcome you aboard!</p>'
        '<p>Best regards,<br>{company_name} Team</p>'
    ))

    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
