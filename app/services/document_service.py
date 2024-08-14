from http.client import HTTPException
from fastapi import HTTPException as FastAPIHTTPException
from sqlalchemy.orm import Session
from app.repository.document_repository import DocumentRepository
from app.schema.user import UserBase
from utils.logger import logger
from utils.classify_pdf import *
from app.schema.document import *
import os

def get_doc_by_id_service(id: int):
    try:
        doc = DocumentRepository.get_doc_by_id(id)
        return doc
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    

# # async def classify_pdf(pdf_path, bucket_name, model_arn, local_output_path):
# async def classify_pdf(document_id: int, bucket_name: str, model_arn: str, local_output_path:str, document: DocumentBase):
#     """Extract text from a PDF, upload it to S3, and classify it using Amazon Comprehend."""
#     # Step 1: Extract text from PDF
#     text = extract_text_from_pdf(document.path)
    
#     # Step 2: Upload the text to S3
#     s3_input_key = f'input/{document.path[:-3]}/input.txt'
#     upload_to_s3(text, bucket_name, s3_input_key)
#     s3_input_uri = f's3://{bucket_name}/{s3_input_key}'

#     # Step 3: Start the classification job
#     s3_output_uri = f's3://{bucket_name}/output/'
#     job_id = start_classification_job(s3_input_uri, s3_output_uri, model_arn)

#     # Step 4: Wait for the job to complete
#     time_index = 0
#     while True:
#         status = get_classification_job_status(job_id)
#         if status in ['COMPLETED', 'FAILED']:
#             break
#         print(f"{job_id}: {status}, time elapsed: {time_index}s. waiting...")
#         logger.info(f"{job_id}: {status}, time elapsed: {time_index}s. waiting...")
#         time_index+=30
#         time.sleep(30)

#     if status == 'COMPLETED':
#         # Step 5: Download and return the results
#         # local_output_path = 'results.json'
#         local_output_path = os.path.join(local_output_path, f"{job_id}")
#         os.makedirs(local_output_path, exist_ok=True)

#         download_classification_results(bucket_name, job_id, local_output_path)
#         logger.info(f"{job_id} tar.gz downloaded")
#         # with open(local_output_path, 'r') as f:
#         #     return f.read()
        
#         predicted_category = print_class(local_output_path)
#         logger.info(f"class({job_id}) = {predicted_category}")
#         update_data = UpdateDocument(classification_status=status, category=predicted_category)
#         DocumentRepository.update_doc_status(document_id,update_data)
#         logger.info(f"{job_id}: db updated")
#         return predicted_category
#     else:
#         update_data = UpdateDocument(classification_status=status, category = "")
#         DocumentRepository.update_doc_status(document_id,update_data)
#         logger.info(f"{job_id}: Classification Failed")
#         raise Exception("Classification job failed")

# async def classify_pdf(pdf_path, bucket_name, model_arn, local_output_path):
async def classify_pdf(docs_w_metadata:  List[DocumentWithMetadata]):
    """Extract text from a PDF, upload it to S3, and classify it using Amazon Comprehend."""
    # job_ids = []
    job_id_flags={}
    for doc_w_metadata in docs_w_metadata:
        text = extract_text_from_pdf(doc_w_metadata.document.path)
        s3_input_key = f'input/{doc_w_metadata.document.path[:-3]}/input.txt'
        upload_to_s3(text, doc_w_metadata.bucket_name, s3_input_key)
        s3_input_uri = f's3://{doc_w_metadata.bucket_name}/{s3_input_key}'
        s3_output_uri = f's3://{doc_w_metadata.bucket_name}/output/'
        job_id_x = start_classification_job(s3_input_uri, s3_output_uri, doc_w_metadata.model_arn)
        # job_ids.append(job_id)
        doc_w_metadata.job_id = job_id_x
        job_id_flags[job_id_x] = 0

    # time_index = 0
    start_time = time.time()
    jobs_in_q = len(job_id_flags)
    while not all(job_id_flags.values()):
        for doc_w_metadata in docs_w_metadata:
            if job_id_flags[doc_w_metadata.job_id] : continue
            status = get_classification_job_status(doc_w_metadata.job_id)
            if status in ['COMPLETED', 'FAILED']:
                job_id_flags[doc_w_metadata.job_id] = 1
                jobs_in_q -= 1
                if status == 'COMPLETED':
                    # local_output_path = os.path.join(doc_w_metadata.local_output_path, f"{doc_w_metadata.job_id}")
                    # os.makedirs(local_output_path, exist_ok=True)
                    local_output_path = f"{doc_w_metadata.local_output_path}-{doc_w_metadata.job_id}.tar.gz"

                    download_classification_results(doc_w_metadata.bucket_name, doc_w_metadata.job_id, local_output_path)
                    logger.info(f"{doc_w_metadata.job_id} tar.gz downloaded")
                    
                    predicted_category = print_class(local_output_path)
                    logger.info(f"class({doc_w_metadata.job_id}) = {predicted_category}")
                    update_data = UpdateDocument(classification_status=status, category=predicted_category)

                    DocumentRepository.update_doc_status(doc_w_metadata.document_id, update_data)
                    logger.info(f"{doc_w_metadata.job_id}: db updated")
                else:
                    update_data = UpdateDocument(classification_status=status, category = "")
                    DocumentRepository.update_doc_status(doc_w_metadata.document_id, update_data)
                    logger.info(f"{doc_w_metadata.job_id}: Classification Failed")
                    raise Exception("Classification job failed")
            logger.info(f"{doc_w_metadata.job_id}: {status}, ")

        logger.info(f"Time Elapsed = {time.time()-start_time}s, Jobs left to classify = {jobs_in_q}")
        # time_index+=30
        time.sleep(30)


    # # Step 1: Extract text from PDF
    # text = extract_text_from_pdf(document.path)
    
    # # Step 2: Upload the text to S3
    # s3_input_key = f'input/{document.path[:-3]}/input.txt'
    # upload_to_s3(text, bucket_name, s3_input_key)
    # s3_input_uri = f's3://{bucket_name}/{s3_input_key}'

    # # Step 3: Start the classification job
    # s3_output_uri = f's3://{bucket_name}/output/'
    # job_id = start_classification_job(s3_input_uri, s3_output_uri, model_arn)

    # # Step 4: Wait for the job to complete
    # time_index = 0
    # while True:
    #     status = get_classification_job_status(job_id)
    #     if status in ['COMPLETED', 'FAILED']:
    #         break
    #     print(f"{job_id}: {status}, time elapsed: {time_index}s. waiting...")
    #     logger.info(f"{job_id}: {status}, time elapsed: {time_index}s. waiting...")
    #     time_index+=30
    #     time.sleep(30)

    # if status == 'COMPLETED':
    #     # Step 5: Download and return the results
    #     # local_output_path = 'results.json'
    #     local_output_path = os.path.join(local_output_path, f"{job_id}")
    #     os.makedirs(local_output_path, exist_ok=True)

    #     download_classification_results(bucket_name, job_id, local_output_path)
    #     logger.info(f"{job_id} tar.gz downloaded")
    #     # with open(local_output_path, 'r') as f:
    #     #     return f.read()
        
    #     predicted_category = print_class(local_output_path)
    #     logger.info(f"class({job_id}) = {predicted_category}")
    #     update_data = UpdateDocument(classification_status=status, category=predicted_category)
    #     DocumentRepository.update_doc_status(document_id,update_data)
    #     logger.info(f"{job_id}: db updated")
    #     return predicted_category
    # else:
    #     update_data = UpdateDocument(classification_status=status, category = "")
    #     DocumentRepository.update_doc_status(document_id,update_data)
    #     logger.info(f"{job_id}: Classification Failed")
    #     raise Exception("Classification job failed")