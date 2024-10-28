from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import os
import json
import datetime
from prompt.review_sort_prompt import sort_review_chain
from langchain_community.document_loaders import PyPDFLoader
from sqlalchemy.orm import Session
from app.models.job import Job  # Replace with actual import path
from app.models.document import Document  # Replace with actual import path
from app.db import get_db  # Replace with actual import path
from utils.logger import logger

router = APIRouter()

# Assuming sort_json_data_based_on_score_desc is a function that sorts JSON data based on score
def sort_json_data_based_on_score_desc(data):
    return sorted(data, key=lambda x: x['match_percentage'], reverse=True)

class ProcessCVRequest(BaseModel):
    job_id: int
    job_desc: str
    weight_skills: int
    weight_experience: int
    weight_education: int
    weight_keywords: int
    weight_accomplishments: int
    num_of_applicants: int

class CVData(BaseModel):
    id: str
    match_percentage: float
    strengths: List[str]
    weaknesses: List[str]
    created_at: str
    category: str

@router.post("/process-cvs/", response_model=List[CVData])
async def process_cvs(request: ProcessCVRequest, db: Session = Depends(get_db)):
    job_id = request.job_id
    job_desc = request.job_desc
    weight_skills = request.weight_skills
    weight_experience = request.weight_experience
    weight_education = request.weight_education
    weight_keywords = request.weight_keywords
    weight_accomplishments = request.weight_accomplishments
    num_of_applicants = request.num_of_applicants

    # Retrieve file paths from the document table using job_id
    documents = db.query(Document).filter(Document.job_id == job_id).all()
    
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found for the given job_id")
    print("Documents found:", documents)
    
    # Ensure file paths are correctly prefixed with the current working directory if they are relative paths
    files = [os.path.join('./', document.path) for document in documents]

    json_data = []
    batch_size = 10  # Adjust batch size as needed

    for i in range(0, len(files), batch_size):
        batch_text = []
        batch_files = files[i:i+batch_size]
        batch_ids = []

        for file in batch_files:
            loader = PyPDFLoader(file)
            docs = loader.load()
            page_content = "\n\n".join(doc.page_content for doc in docs)
            batch_text.append({
                "cv_text": page_content, 
                "job_desc": job_desc,
                "weight_skills": weight_skills,
                "weight_experience": weight_experience,
                "weight_education": weight_education,
                "weight_keywords": weight_keywords,
                "weight_accomplishments": weight_accomplishments
            })
            batch_ids.append(os.path.splitext(os.path.basename(file))[0])  # Append the file name without extension

        # Call the batch method without await if it is not asynchronous
        ans = sort_review_chain.batch(batch_text)

        for j in range(len(ans)):
            convert_ans = json.loads(ans[j])
            convert_ans['id'] = batch_ids[j]
            convert_ans['created_at'] = datetime.datetime.now().isoformat()
            json_data.append(convert_ans)
    
    print("JSON data:", json_data)        

    sorted_data = sort_json_data_based_on_score_desc(json_data)

    # Categorize the applicants based on the num_of_applicants
    num_best_match = int(num_of_applicants * 0.2)
    num_medium_match = int(num_of_applicants * 0.3)
    num_low_match = num_of_applicants - num_best_match - num_medium_match

    for i, data in enumerate(sorted_data):
        if i < num_best_match:
            data['category'] = 'Best Match'
        elif i < num_best_match + num_medium_match:
            data['category'] = 'Medium Match'
        else:
            data['category'] = 'Low Match'

    return sorted_data




# New endpoint to retrieve all job details for a specific user
class JobData(BaseModel):
    job_id: int
    name: str
    description: str

@router.get("/user/{user_id}/jobs", response_model=List[JobData])
async def get_jobs_by_user_id(user_id: int, db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.user_id == user_id).all()
    
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found for the given user_id")
    
    job_details = [{"job_id": job.id, "name": job.name, "description": job.description} for job in jobs]
    
    return job_details