from http.client import HTTPException
from app.repository.document_repository import DocumentRepository
from utils.logger import logger
from utils.classify_pdf import *
from utils.helper import move_file_to_classified_directory
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
    


def initiate_classification_process(path: str, bucket_name: str, model_arn: str):
    """Extract text from a PDF, upload it to S3, and classify it using Amazon Comprehend."""

    # Extract Text
    text = extract_text_from_pdf(path)

    #Upload to S3
    s3_input_key = f'input/{path[:-3]}/input.txt'
    upload_to_s3(text, bucket_name, s3_input_key)
    s3_input_uri = f's3://{bucket_name}/{s3_input_key}'
    s3_output_uri = f's3://{bucket_name}/output/'
    
    # Send to document to classify
    job_id_x = start_classification_job(s3_input_uri, s3_output_uri, model_arn)
    return job_id_x


def classify_pdf(doc_w_metadata:  DocumentWithMetadata):
    """
    Trigger the classification of a document using Amazon Comprehend.

    This function is called when a document needs to be classified. It will
    trigger the classification process by calling the
    initiate_classification_process function with the appropriate parameters.

    Args:
        doc_w_metadata (DocumentWithMetadata): The document to be classified,
            including its path, bucket name, and model ARN.

    Returns:
        str: The job ID of the classification job.
    """
    return initiate_classification_process(
        doc_w_metadata.document.path, doc_w_metadata.bucket_name, doc_w_metadata.model_arn
    )


def trigger_sub_classification(job_id: int) -> None:
    """Trigger sub-classification of a document.

    This function is called when a document has been classified as SOFTWARE-ENGINEER.
    It will trigger the sub-classification process by calling the
    initiate_classification_process function with the appropriate parameters.

    Args:
        job_id (int): The comprehend job id of the document
    """
    document = DocumentRepository.get_doc_by_comprehend_job_id(job_id)

    # Trigger sub-classification
    sub_classification_job_id = initiate_classification_process(
        document.path, l2_bucket_name, l2_model_arn
    )

    # Update the document status
    DocumentRepository.update_doc_status(
        document.id,
        UpdateDocument(
            classification_status="IN PROGRESS",
            comprehend_job_id=sub_classification_job_id,
        ),
    )

def process_record(record: dict) -> None:
    """Process a single S3 bucket notification record"""
    bucket_name = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    if not key.endswith(".tar.gz"):
        logger.info(f"Skipping non-tar.gz file: {key}")
        return

    job_id = key.split("/")[1].split("-")[2]
    local_output_path = f"data/s3_output_zips/{job_id}.tar.gz"

    logger.info(f"Processing record: {job_id}")
    # Download the classification output file
    download_classification_results(bucket_name, key, local_output_path)

    # Get the predicted category or sub-category from the tar file
    if bucket_name == l1_bucket_name:
        predicted_category = find_out_class_from_tar(local_output_path)
        update_data = UpdateDocumentComprehend(classification_status="COMPLETED", category=predicted_category)

    
    elif bucket_name == l2_bucket_name:
        predicted_category = find_out_sub_class_from_tar(local_output_path)
        update_data = UpdateDocumentComprehend(classification_status="COMPLETED", sub_category=predicted_category)

    # Update the document status in the database
    doc = DocumentRepository.update_doc_by_comprehend_job_id(job_id, update_data)
    new_path = move_file_to_classified_directory(predicted_category, doc.path)
    doc = DocumentRepository.update_doc_status(doc.id, UpdateDocument(path=new_path))

    if predicted_category == "SOFTWARE-ENGINEER":
        # If the category is SOFTWARE-ENGINEER, trigger sub-classification
        trigger_sub_classification(job_id)
        
    # Delete the downloaded tar file
    if os.path.exists(local_output_path):
        os.remove(local_output_path)
    
