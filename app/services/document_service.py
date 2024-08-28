from http.client import HTTPException
from app.repository.document_repository import DocumentRepository
from utils.logger import logger
from utils.classify_pdf import *
from utils.helper import move_file_to_classified_directory
from app.schema.document import *
import os
from app.config import l2_bucket_name, l2_model_arn, local_pdf_directory
import httpx
from app.services.elastic_search_helper import add_cv_file_to_index
from app.repository.job_repository import JobRepository
from utils.websocket import manager

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


async def handle_sns_subscription_confirmation(request_data):
    """
    Handle SNS subscription confirmation by confirming the subscription
    and raising an exception if the confirmation fails.

    """
    # Check if the request data contains the subscription URL
    if "SubscribeURL" in request_data:
        subscribe_url = request_data["SubscribeURL"]

        # Confirm the subscription by sending a GET request to the subscription URL
        async with httpx.AsyncClient() as client:
            response = await client.get(subscribe_url)

        # Raise an exception if the subscription confirmation fails
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Subscription confirmation failed")


async def handle_sns_records(request_data):
    """
    Handle records from SNS by processing each record.
    """
    # Check if the request data contains the records
    if "Records" not in request_data:
        return

    # Get the records from the request data
    records = request_data["Records"]

    # Process each record
    for record in records:
        # Process the record
        process_record(record)

def process_record(record: dict) -> None:
    """
    Process a single S3 bucket notification record.

    Args:
        record (dict): The S3 bucket notification record.
    """
    # Extract the bucket name and object key from the record
    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']

    # Check if the object key ends with ".tar.gz" and return if it doesn't
    if not object_key.endswith(".tar.gz"):
        return

    # Get the job ID from the object key
    job_id = object_key.split("/")[1].split("-")[2]

    # Create the output path for the tar file
    output_path = f"data/s3_output_zips/{job_id}.tar.gz"

    # Download the classification output file to the local directory
    download_classification_results(bucket_name, object_key, output_path)

    # Initialize the update data for the document
    update_data = None

    # Check if the bucket name is for level 1 classification
    if bucket_name == l1_bucket_name:
        # Get the category from the tar file and update the update data
        category = find_out_class_from_tar(output_path)
        update_data = UpdateDocumentComprehend(
            classification_status="COMPLETED", category=category
        )
    # Check if the bucket name is for level 2 classification
    elif bucket_name == l2_bucket_name:
        # Get the sub-category from the tar file and update the update data
        sub_category = find_out_sub_class_from_tar(output_path)
        update_data = UpdateDocumentComprehend(
            classification_status="COMPLETED", sub_category=sub_category
        )

    # Update the document in the database with the update data
    document = DocumentRepository.update_doc_by_comprehend_job_id(job_id, update_data)

    # Create the new path for the classified document
    new_path = move_file_to_classified_directory(
        category if bucket_name == l1_bucket_name else sub_category, document.path
    )

    # Update the document status in the database
    DocumentRepository.update_doc_status(
        document.id, UpdateDocument(path=new_path)
    )

    # Get the user ID associated with the job
    user_id = JobRepository.get_user_by_job_id(document.job_id)

    # Check if the category is SOFTWARE-ENGINEER
    if category == "SOFTWARE-ENGINEER":
        # Trigger sub-classification
        trigger_sub_classification(job_id)
    else:
        # Add the cv file to the index and broadcast the user ID
        add_cv_file_to_index(new_path)
        manager.broadcast(str(user_id))

    # Remove the downloaded tar file
    if os.path.exists(output_path):
        os.remove(output_path)
    
