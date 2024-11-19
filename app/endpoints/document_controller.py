from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from app.db import get_db
from app.schema.document import *
from app.services.document_service import *
from app.helpers.custom_exception_handler import *
from utils.helper import custom_response_handler
import aiofiles
import uuid
from app.models.job import Job  
from app.repository.document_repository import DocumentRepository
from datetime import datetime
from app.config import l1_model_arn, l1_bucket_name, local_pdf_directory
from app.services.elastic_search_helper import add_cv_file_to_index
from apscheduler.triggers.cron import CronTrigger
from utils.scheduler import scheduler
from utils.websocket import manager
import time
import hashlib
from sqlalchemy.orm import Session
from app.models.document import Document
import shutil
from app.services.job_applications_service import store_job_application
from app.services.elastic_search_helper import delete_cv_from_index
from app.endpoints.email_controller import send_email
from pathlib import Path
import uuid
from utils.background_tasks import process_files_in_background
static_directory = 'static'

router = APIRouter()

@router.get("/{document_id}", response_model=DocumentBase)
async def get_doc_by_id(document_id: int):
    try:
        doc = await get_doc_by_id_service(document_id)
        return custom_response_handler(200, "Document retrieved successfully", doc)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    


@router.post("/upload-pdfs/")
async def upload_pdf(email:str,job_id: int, files: list[UploadFile] = File(...),db: Session = Depends(get_db),background_tasks: BackgroundTasks = BackgroundTasks()):
    save_directory = Path(f"./static")
    save_directory.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    saved_files = []

    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Generate a unique filename
        unique_id = uuid.uuid4()
        file_extension = Path(file.filename)
        safe_filename = f"{job_id}_{unique_id}_{file_extension}"

        # Construct the path where the file will be saved
        save_path = save_directory / safe_filename

        # Save the file
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Store the saved file's relative path
        saved_files.append(str(save_path))

        # Optionally, add database logic here to associate the file with a record
        # Example: Insert a record into `cv_applications` (requires additional logic)
    background_tasks.add_task(process_files_in_background, save_path, email, job_id, db,background_tasks)    

    return {"message": "Files uploaded successfully", "saved_files": saved_files}

    # # Create the local directory to store the PDF files if it doesn't exist
    # os.makedirs(local_pdf_directory, exist_ok=True)
    # os.makedirs(static_directory, exist_ok=True)  # Create the static folder if it doesn't exist
    
    # Job_info=db.query(Job).filter_by(id=job_id).first()
    # if not Job_info:
    #     raise HTTPException(status_code=404, detail="Job not found")
    # try:
    #     send_email("nabibpallab22@gmail.com",email,Job_info.name)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}") 
    # try:
    #     for file in files:
    #         # Get the original filename and create a new filename with a timestamp
    #         original_filename = file.filename
    #         name, ext = os.path.splitext(original_filename)
    #         file_name = f"{name}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"
    #         file_path = os.path.join(local_pdf_directory, file_name)

    #         # Write the file to the local directory
    #         async with aiofiles.open(file_path, 'wb') as out_file:
    #             content = await file.read()
    #             await out_file.write(content)
                
    #         # Copy the file to the static folder
    #         static_file_path = os.path.join(static_directory, file_name)
    #         store_job_application(job_id, file_name, email, db)
    #         shutil.copy(file_path, static_file_path)  # Copy the file to the static directory    
                
    #         # Generate the SHA-256 hash of the PDF content
    #         pdf_hash = hashlib.sha256(content).hexdigest()
            
    #         # Check if the document with the same hash already exists in the database
    #         existing_doc = db.query(Document).filter_by(pdf_hash=pdf_hash).first() 
            
    #         if existing_doc:
    #             # If the document already exists, update the job_id and skip classification
    #             existing_doc.job_id = job_id
    #             existing_doc.updated_at = datetime.utcnow()
    #             db.commit()
    #             logger.info(f"PDF {original_filename} already classified, skipping classification.")
    #             continue   

    #         # Create a new document in the database
    #         doc = DocumentBase(
    #             path=file_path,
    #             created_at=datetime.utcnow(),
    #             updated_at=datetime.utcnow(),
    #             summary="",
    #             category="",
    #             sub_category="",
    #             classification_status="IN PROGRESS",
    #             comprehend_job_id="",
    #             job_id = job_id,
    #             pdf_hash=pdf_hash
    #         )

    #         # Create a DocumentWithMetadata object to be used for classification
    #         doc_w_metadata = DocumentWithMetadata(
    #             bucket_name=l1_bucket_name,
    #             model_arn=l1_model_arn,
    #             document=doc,
    #             file_name=file_name,
    #             local_output_path=f"data/s3_output_zips/{file_name}",
    #         )

    #         # Trigger the classification process
    #         job_id = classify_pdf(doc_w_metadata)
    #         doc.comprehend_job_id = job_id
    #         DocumentRepository.add_file(doc)

    #     # Log the successful upload and classification
    #     logger.info("PDF files uploaded successfully and classification started.")
    #     return {"message": "PDF files uploaded successfully and classification started."}
    # except HTTPException as e:
    #     # Log any HTTP errors
    #     logger.info(f'An HTTP error occurred: \n {str(e)}')
    #     raise e
    # except Exception as e:
    #     # Log any errors
    #     logger.info(f'An error occurred: \n {str(e)}')
    #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.post("/sns-endpoint/")
async def handle_sns_endpoint(request: Request):
    logger.info("Received SNS endpoint request.")
    request_data = await request.json()

    await handle_sns_subscription_confirmation(request_data)
    await handle_sns_records(request_data)
    await manager.broadcast("0")

    return {"status": "success"}




@router.get("/document/generate-json")
async def generate_json(db: Session = Depends(get_db)):
    try:
        documents = db.query(Document).all()

        base_url = "http://localhost:7705/static"
        json_structure = {"uploaded_pdfs": {}}

        for doc in documents:
            # Split the path
            path_parts = doc.path.split("/")
            
            if len(path_parts) < 3:  # Ensure there are at least 3 parts (for category)
                continue  # Skip this document if the path is invalid or incorrectly formatted

            category = path_parts[2]  # E.g., "SOFTWARE-ENGINEER" or "Business_Analyst"
            pdf_name = path_parts[-1]  # The file name, e.g., "Tahmid_Rahman_Cv-6_20240905102248.pdf"

            # PDF Link
            pdf_link = f"{base_url}/{pdf_name}"

            # Initialize categories if they don't exist
            if category not in json_structure["uploaded_pdfs"]:
                json_structure["uploaded_pdfs"][category] = []

            # Check if sub-category exists (only for categories with sub-categories)
            if len(path_parts) > 3:  # Only check for sub-category if it exists
                sub_category = path_parts[3]  # E.g., "Network"

                # Check if sub-category exists and create the structure if needed
                sub_category_dict = next((item for item in json_structure["uploaded_pdfs"][category] if sub_category in item), None)

                if not sub_category_dict:
                    sub_category_dict = {sub_category: []}
                    json_structure["uploaded_pdfs"][category].append(sub_category_dict)

                # Add the PDF name and link under the sub-category
                sub_category_dict[sub_category].append({"PDF Name": pdf_name, "PDF Link": pdf_link})
            else:
                # If there's no sub-category, add the PDF directly under the category
                json_structure["uploaded_pdfs"][category].append({"PDF Name": pdf_name, "PDF Link": pdf_link})

        return json_structure

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    

@router.delete("/document/{document_id}")
async def delete_document(document_id: str, db: Session = Depends(get_db)):
    """
    Delete a document by document ID.
    - document_id: The ID of the document to delete.
    """
    try:
        # Fetch the file path from the database using the document_id
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        file_path = document.path
        
               # Extract the document_id from the file path
        extracted_document_id = os.path.splitext(os.path.basename(file_path))[0]
        
        # print(extracted_document_id)


        # Delete the file from the filesystem
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File {file_path} deleted from filesystem")
        else:
            logger.warning(f"File {file_path} not found in filesystem")

        # Delete the document from the Elasticsearch index
        delete_cv_from_index(extracted_document_id)
        logger.info(f"Document with ID {extracted_document_id} deleted from Elasticsearch index")

        # Delete the document record from the database
        db.delete(document)
        db.commit()
        logger.info(f"Document with ID {document_id} deleted from database")

        return {"status": "success", "message": f"Document with ID {document_id} deleted successfully"}

    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.error(f"Exception {e} occurred while deleting document with ID {document_id}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")    
    