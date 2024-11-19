from prompt.evaluation_prompt import talent_evaluation_chain
from langchain_community.document_loaders import PyPDFLoader
from app.models.job import Job
from app.endpoints.cv_applications_controller import create_cvapplication
import hashlib
import json
import os
from datetime import datetime
from app.services.elastic_search_helper import add_cv_file_to_index



def generate_file_hash(file_path: str) -> str:
    """Generate SHA256 hash for the CV file"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):  # Read the file in chunks
            sha256.update(chunk)
    return sha256.hexdigest()

def process_files_in_background(save_path: str, email: str, job_id: int, db,background_tasks):
    print("Processing files in the background...")

    # Construct the full file path for the uploaded CV
    file_path = os.path.join('./', save_path)
    print(f"Processing file: {file_path}")
    
    # Load and extract text content from the PDF file
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    page_content = "\n\n".join(doc.page_content for doc in docs)

    # Get job details from the database based on job_id
    get_job = db.query(Job).filter(Job.id == job_id).first()
    if not get_job:
        print(f"Job with ID {job_id} not found.")
        return

    # Extract job description and title for evaluation
    job_desc = get_job.description
    job_title = get_job.name
    
    # Perform talent evaluation
    evaluation_result = talent_evaluation_chain.invoke({
        "cv_text": page_content,
        "job_description": job_desc,
        "job_title": job_title
    })

    # Load the evaluation result into JSON format
    evaluation_result = json.loads(evaluation_result)
    
        
    # Extract relevant fields from the evaluation result
    match_percentage = evaluation_result['cv_match_percentage']
    key_strengths = evaluation_result['key_strengths']
    areas_of_concern = evaluation_result['areas_of_concern']
    detailed_analysis = evaluation_result['detailed_analysis']

    # Generate the hash for the CV file to store in the database
    cv_hash = generate_file_hash(file_path)
    
    #convert match percentage to float
    match_percentage = float(match_percentage)
    
    if match_percentage >= 85:
        current_category = "best_match"
    elif match_percentage >= 70:
        current_category = "medium_match"
    elif match_percentage >= 60:
        current_category = "low_match"
    else:
        current_category = "miscellaneous"
    
       # Prepare the CV application data to be inserted into the database
    cv_application_data = {
        "email": email,
        "job_id": job_id,
        "current_category": current_category,
        "cv_match_percentage": match_percentage,
        "key_strengths": key_strengths,
        "areas_of_concern": areas_of_concern,
        "detailed_analysis": detailed_analysis,
        "cv_hash": cv_hash,
        "file_path": str(save_path),  # This can be the path to the uploaded file in the server
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    # Call the function to create a new CV application record
    add_cv_file_to_index(save_path)
    background_tasks.add_task(create_cvapplication, cv_application_data, db)

    print("Background processing complete.")