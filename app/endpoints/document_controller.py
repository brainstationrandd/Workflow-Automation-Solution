from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from app.db import get_db
from app.schema.document import *
from app.services.document_service import *
from app.helpers.custom_exception_handler import *
from utils.helper import custom_response_handler
import aiofiles
import uuid
from app.repository.document_repository import DocumentRepository
from datetime import datetime
from app.config import l1_model_arn, l1_bucket_name, local_pdf_directory
from app.services.elastic_search_helper import add_cv_file_to_index
from apscheduler.triggers.cron import CronTrigger
from utils.scheduler import scheduler
from utils.websocket import manager
import time

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
async def upload_pdf(job_id: int, files: list[UploadFile] = File(...)):

    # Create the local directory to store the PDF files if it doesn't exist
    os.makedirs(local_pdf_directory, exist_ok=True)

    try:
        for file in files:
            # Get the original filename and create a new filename with a timestamp
            original_filename = file.filename
            name, ext = os.path.splitext(original_filename)
            file_name = f"{name}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"
            file_path = os.path.join(local_pdf_directory, file_name)

            # Write the file to the local directory
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            # Create a new document in the database
            doc = DocumentBase(
                path=file_path,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                summary="",
                category="",
                sub_category="",
                classification_status="IN PROGRESS",
                comprehend_job_id="",
                job_id = job_id
            )

            # Create a DocumentWithMetadata object to be used for classification
            doc_w_metadata = DocumentWithMetadata(
                bucket_name=l1_bucket_name,
                model_arn=l1_model_arn,
                document=doc,
                file_name=file_name,
                local_output_path=f"data/s3_output_zips/{file_name}",
            )

            # Trigger the classification process
            job_id = classify_pdf(doc_w_metadata)
            doc.comprehend_job_id = job_id
            DocumentRepository.add_file(doc)

        # Log the successful upload and classification
        logger.info("PDF files uploaded successfully and classification started.")
        return {"message": "PDF files uploaded successfully and classification started."}
    except HTTPException as e:
        # Log any HTTP errors
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        # Log any errors
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.post("/sns-endpoint/")
async def handle_sns_endpoint(request: Request):
    request_data = await request.json()

    await handle_sns_subscription_confirmation(request_data)
    await handle_sns_records(request_data)

    return {"status": "success"}






