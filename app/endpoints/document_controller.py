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
from app.config import l1_model_arn, l1_bucket_name
import asyncio
from functools import partial
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
async def upload_pdf(background_tasks: BackgroundTasks, files: list[UploadFile] = File(...), db: Session = Depends(get_db) ):
    save_directory = "data/uploaded_pdfs"
    os.makedirs(save_directory, exist_ok=True)
    try:
        docs_w_metadata = []
        for file in files:
            file_path = os.path.join(save_directory, f"{uuid.uuid4()}.pdf")
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            doc = DocumentBase(
                path = file_path,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                summary = "",
                category = "",
                classification_status= "IN PROGRESS"
            )
            
            db_file = DocumentRepository.add_file(doc)

            doc_w_metadata = DocumentWithMetadata(
                document_id = db_file.id,
                bucket_name = l1_bucket_name,
                model_arn = l1_model_arn,
                document = doc,
                local_output_path = f"data/s3_output_zips/{uuid.uuid4()}",
                job_id = ''
            )

            docs_w_metadata.append(doc_w_metadata)

            # task = asyncio.create_task(
            #             partial( classify_pdf,
            #                             bucket_name = l1_bucket_name,
            #                             model_arn = l1_model_arn,
            #                             document = doc,
            #                             local_output_path = os.path.join("data/s3_output_zips",f"{uuid.uuid4()}")
                                    
            #                     ))()
            # tasks.append(task)
            # background_tasks.add_task(classify_pdf,
            #                         document_id = db_file.id,
            #                         bucket_name = l1_bucket_name,
            #                         model_arn = l1_model_arn,
            #                         document = doc,
            #                         local_output_path = os.path.join("data/s3_output_zips",f"{uuid.uuid4()}")
                                    
            #                         )
        background_tasks.add_task(classify_pdf, docs_w_metadata = docs_w_metadata)
        # background_tasks.add_task(asyncio.gather(*tasks))
        # await asyncio.gather(*tasks)
        logger.info("PDF files uploaded successfully and classification started.")
        return {"message": "PDF files uploaded successfully and classification started."}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    