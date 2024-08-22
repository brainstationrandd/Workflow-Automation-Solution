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
import httpx
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
async def upload_pdf(background_tasks: BackgroundTasks, files: list[UploadFile] = File(...)):
    # save_directory = "data/uploaded_pdfs"
    os.makedirs(local_pdf_directory, exist_ok=True)
    try:
        # docs_w_metadata = []
        for file in files:
            original_filename = file.filename
            name, ext = os.path.splitext(original_filename)
            # file_path = os.path.join(save_directory, f"{uuid.uuid4()}.pdf")
            file_name = f"{name}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"
            file_path = os.path.join(local_pdf_directory, file_name)
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            doc = DocumentBase(
                path = file_path,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                summary = "",
                category = "",
                sub_category = "",
                classification_status= "IN PROGRESS",
                comprehend_job_id=""
            )
            
            # db_file = DocumentRepository.add_file(doc)

            doc_w_metadata = DocumentWithMetadata(
                # document_id = db_file.id,
                bucket_name = l1_bucket_name,
                model_arn = l1_model_arn,
                document = doc,
                file_name = file_name,
                local_output_path = f"data/s3_output_zips/{file_name}",
                # job_id = ''
            )
            
            job_id = classify_pdf(doc_w_metadata)
            doc.comprehend_job_id = job_id
            DocumentRepository.add_file(doc)

            # docs_w_metadata.append(doc_w_metadata)

        # background_tasks.add_task(classify_pdf, docs_w_metadata = docs_w_metadata)

        logger.info("PDF files uploaded successfully and classification started.")
        return {"message": "PDF files uploaded successfully and classification started."}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.post("/sns-endpoint/")
async def sns_endpoint(request: Request):
    data = await request.json()

    # Handle SNS subscription confirmation
    if "SubscribeURL" in data:
        subscribe_url = data["SubscribeURL"]
        # Confirm the subscription by making a GET request to the SubscribeURL
        async with httpx.AsyncClient() as client:
            response = await client.get(subscribe_url)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Subscription confirmation failed")

    # Handle SNS notifications
    # if "Message" in data:
    #     message = data["Message"]
    #     # Process the message, e.g., log it or trigger another action
    #     logger.info(f"Received SNS message: {message}")
    #     print(f"Received SNS message: {message}")

    if "Records" in data:
        records = data["Records"]
        for record in records:
            process_record(record)

    print(data)
    logger.info(f"Entire Received SNS message: {data}")

    return {"status": "success"}



# https://b50d-103-95-99-146.ngrok-free.app/api/document/sns-endpoint/
# arn:aws:sns:us-east-1:905418236735:classification