from http.client import HTTPException
from app.repository.document_repository import DocumentRepository
from utils.logger import logger
from utils.classify_pdf import *
from utils.helper import move_file_classified_directory
from app.schema.document import *
import os
from app.config import l2_bucket_name, l2_model_arn, local_pdf_directory
import shutil

def get_doc_by_id_service(id: int):
    try:
        doc = DocumentRepository.get_doc_by_id(id)
        return doc
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
def classify_pdf(doc_w_metadata:  DocumentWithMetadata):
    """Extract text from a PDF, upload it to S3, and classify it using Amazon Comprehend."""
    # job_id_flags = create_jobs(docs_w_metadata)
    # return job_id_flags

    # job_id_flags={}
    # for doc_w_metadata in docs_w_metadata:
        # Extract Text
    text = extract_text_from_pdf(doc_w_metadata.document.path)

    #Upload to S3
    s3_input_key = f'input/{doc_w_metadata.document.path[:-3]}/input.txt'
    upload_to_s3(text, doc_w_metadata.bucket_name, s3_input_key)
    s3_input_uri = f's3://{doc_w_metadata.bucket_name}/{s3_input_key}'
    s3_output_uri = f's3://{doc_w_metadata.bucket_name}/output/'
    
    # Send to document to classify
    job_id_x = start_classification_job(s3_input_uri, s3_output_uri, doc_w_metadata.model_arn)
    return job_id_x
    # DocumentRepository.update_doc_status(doc_w_metadata.document_id, UpdateDocument(comprehend_job_id = job_id_x))
        # doc_w_metadata.job_id = job_id_x
        # job_id_flags[job_id_x] = 0
    # return job_id_flags

    # sub_docs_w_metadata = []
    # start_time = time.time()
    # jobs_in_q = len(job_id_flags)
    # while not all(job_id_flags.values()):
    #     for doc_w_metadata in docs_w_metadata:
    #         if job_id_flags[doc_w_metadata.job_id] : continue
    #         status = get_classification_job_status(doc_w_metadata.job_id)

    #         #wait till classification is complete
    #         if status in ['COMPLETED', 'FAILED']:
    #             job_id_flags[doc_w_metadata.job_id] = 1
    #             jobs_in_q -= 1
    #             if status == 'COMPLETED':
    #                 local_output_path = f"{doc_w_metadata.local_output_path}-{doc_w_metadata.job_id}.tar.gz"
                    
    #                 #download classification data
    #                 download_classification_results(doc_w_metadata.bucket_name, doc_w_metadata.job_id, local_output_path)
    #                 logger.info(f"{doc_w_metadata.job_id} tar.gz downloaded")
                    
    #                 predicted_category = print_class(local_output_path)
    #                 doc_w_metadata.document.category = predicted_category
    #                 logger.info(f"class({doc_w_metadata.job_id}) = {predicted_category}")
                    
    #                 #Move pdf to classified directory
    #                 classified_directory = move_file_classified_directory(doc_w_metadata.file_name, predicted_category)

    #                 #update db according to category
    #                 update_data = UpdateDocument(classification_status = status, category = predicted_category, path = classified_directory)
    #                 doc_w_metadata.document.path = classified_directory
    #                 DocumentRepository.update_doc_status(doc_w_metadata.document_id, update_data)
    #                 logger.info(f"{doc_w_metadata.job_id}: db updated")

    #                 #store CVs of Software Engineers
    #                 if predicted_category == "SOFTWARE-ENGINEER":
    #                     sub_doc_w_metadata = DocumentWithMetadata(
    #                         document_id = doc_w_metadata.document_id,
    #                         bucket_name = l2_bucket_name,
    #                         model_arn = l2_model_arn,
    #                         document = doc_w_metadata.document,
    #                         file_name=doc_w_metadata.file_name,
    #                         local_output_path = doc_w_metadata.local_output_path,
    #                         job_id = ''
    #                     )
    #                     sub_docs_w_metadata.append(sub_doc_w_metadata)
    #             else:
    #                 #updaate db
    #                 update_data = UpdateDocument(classification_status = status, category = "")
    #                 DocumentRepository.update_doc_status(doc_w_metadata.document_id, update_data)
    #                 logger.info(f"{doc_w_metadata.job_id}: Classification Failed")
    #                 raise Exception("Classification job failed")
            
    #         logger.info(f"{doc_w_metadata.job_id}: {status}, ")

    #     logger.info(f"Time Elapsed = {time.time()-start_time}s, Jobs left to classify = {jobs_in_q}")
    #     if not jobs_in_q: break
    #     time.sleep(30)

    # if len(sub_docs_w_metadata):
    #     sub_classify_pdf(docs_w_metadata=sub_docs_w_metadata)

# def sub_classify_pdf(docs_w_metadata:  List[DocumentWithMetadata]):
#     job_id_flags = create_jobs(docs_w_metadata)

#     start_time = time.time()
#     jobs_in_q = len(job_id_flags)
#     while not all(job_id_flags.values()):
#         for doc_w_metadata in docs_w_metadata:
#             if job_id_flags[doc_w_metadata.job_id] : continue
#             status = get_classification_job_status(doc_w_metadata.job_id)

#             #wait for classification job to be done
#             if status in ['COMPLETED', 'FAILED']:
#                 job_id_flags[doc_w_metadata.job_id] = 1
#                 jobs_in_q -= 1
#                 if status == 'COMPLETED':
#                     local_output_path = f"{doc_w_metadata.local_output_path}-{doc_w_metadata.job_id}.tar.gz"

#                     download_classification_results(doc_w_metadata.bucket_name, doc_w_metadata.job_id, local_output_path)
#                     logger.info(f"{doc_w_metadata.job_id} tar.gz downloaded")
                    
#                     predicted_category = print_sub_class(local_output_path)
#                     doc_w_metadata.document.sub_category = predicted_category
#                     logger.info(f"class({doc_w_metadata.job_id}) = {predicted_category}")
                    
#                     #Move pdf to classified directory
#                     sub_classified_directory = move_file_classified_directory(doc_w_metadata.file_name, predicted_category, old_directory=os.path.join(local_pdf_directory,"SOFTWARE-ENGINEER"))

#                     update_data = UpdateDocument(classification_status=status, sub_category=predicted_category, path = sub_classified_directory)
#                     doc_w_metadata.document.path = sub_classified_directory

#                     #Update db for subclassification
#                     DocumentRepository.update_doc_status(doc_w_metadata.document_id, update_data)
#                     logger.info(f"{doc_w_metadata.job_id}: db updated")

#                 else:
#                     update_data = UpdateDocument(classification_status=status, sub_category = "")
#                     DocumentRepository.update_doc_status(doc_w_metadata.document_id, update_data)
#                     logger.info(f"{doc_w_metadata.job_id}: Classification Failed")
#                     raise Exception("Classification job failed")
#             logger.info(f"{doc_w_metadata.job_id}: {status}, ")

#         logger.info(f"Time Elapsed = {time.time()-start_time}s, Jobs left to classify = {jobs_in_q}")
#         if not jobs_in_q: return
#         time.sleep(30)

def sub_classify_pdf(job_id):
    document = DocumentRepository.get_doc_by_comprehend_job_id(job_id)
    
    text = extract_text_from_pdf(document.path)
    #Upload to S3
    s3_input_key = f'input/{document.path[:-3]}/input.txt'
    upload_to_s3(text, l2_bucket_name, s3_input_key)
    s3_input_uri = f's3://{l2_bucket_name}/{s3_input_key}'
    s3_output_uri = f's3://{l2_bucket_name}/output/'
    
    # Send to document to classify
    job_id_x = start_classification_job(s3_input_uri, s3_output_uri, l2_model_arn)
    DocumentRepository.update_doc_status(document.id, UpdateDocument(classification_status = "IN_PROGRESS", comprehend_job_id = job_id_x))

def process_record(record):
    key = record['s3']['object']['key']
    if key.endswith(".tar.gz"):
        bucket_name = record['s3']['bucket']['name']
        job_id = record['s3']['object']['key'].split("/")[1].split("-")[2]
        local_output_path = f"data/s3_output_zips/{job_id}.tar.gz"
        download_classification_results(bucket_name,key,local_output_path)
        logger.info(f"output.tar.gz downloaded for {job_id}")
        if bucket_name in l1_bucket_name:
            predicted_category = find_out_class_from_tar(local_output_path)
            logger.info(f"category ({job_id}) = {predicted_category}")
            upadte_data = UpdateDocumentComprehend(classification_status = "COMPLETED", category = predicted_category)
            DocumentRepository.update_doc_by_comprehend_job_id(job_id=job_id, document = upadte_data)

        # elif bucket_name in l2_bucket_name:
        #     predicted_category = find_out_class_from_tar(local_output_path)
        #     logger.info(f"sub_category ({job_id}) = {predicted_category}")
        #     doc = UpdateDocumentComprehend(classification_status = "COMPLETED", sub_category = predicted_category)
        #     DocumentRepository.update_doc_by_comprehend_job_id(job_id, doc)
        #     logger.info(f"db updated for {job_id} subcategory")


        if os.path.exists(local_output_path): os.remove(local_output_path)
        logger.info(f"output.tar.gz deleted for {job_id}")
