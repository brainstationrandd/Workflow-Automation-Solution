import boto3
import tarfile
import json
import PyPDF2
import os
import time
from app.config import *
from utils.llms import session
from app.schema.document import *


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyPDF2."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def upload_to_s3(text, bucket_name, s3_key):
    """Upload the text to an S3 bucket."""
    s3 = session.client('s3')
    s3.put_object(Body=text, Bucket=bucket_name, Key=s3_key)

def start_classification_job(s3_input_uri, s3_output_uri, model_arn):
    """Start a document classification job using Amazon Comprehend."""
    comprehend = session.client('comprehend')
    response = comprehend.start_document_classification_job(
        InputDataConfig={
            'S3Uri': s3_input_uri,
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': s3_output_uri
        },
        DataAccessRoleArn=comprehendAITeam,  # IAM Role with necessary permissions
        DocumentClassifierArn=model_arn,
        # JobCompletionNotificationChannel={
            
        # }
    )
    return response['JobId']

def get_classification_job_status(job_id):
    """Check the status of the document classification job."""
    comprehend = session.client('comprehend')
    response = comprehend.describe_document_classification_job(
        JobId=job_id
    )
    return response['DocumentClassificationJobProperties']['JobStatus']

def print_class(location):
    # location = os.path.join(location, "s3_output.tar.gz")
    with tarfile.open(location, 'r:gz') as tar:
        # Loop through the files in the tar archive
        for member in tar.getmembers():
            # Check if the file is a .jsonl file
            if member.isfile() and member.name.endswith('.jsonl'):
                # Extract the file
                f = tar.extractfile(member)
                # Read and decode lines from the file
                for line in f:
                    json_data = json.loads(line.decode('utf-8'))
                    print(json_data['Classes'][0])
                    return str(json_data['Classes'][0]['Name'])
                

                
def print_sub_class(location, threshold = sub_category_threshold):
    # location = os.path.join(location, "s3_output.tar.gz")
    with tarfile.open(location, 'r:gz') as tar:
        # Loop through the files in the tar archive
        for member in tar.getmembers():
            # Check if the file is a .jsonl file
            if member.isfile() and member.name.endswith('.jsonl'):
                # Extract the file
                f = tar.extractfile(member)
                # Read and decode lines from the file
                for line in f:
                    json_data = json.loads(line.decode('utf-8'))
                    print(json_data['Labels'][0])
                    ans=""
                    for label in json_data['Labels']:
                        name = label["Name"]
                        if label["Score"] >= threshold : ans = f"{ans}|{name}"
                    return str(ans[1:])


def download_classification_results(s3_output_uri, job_id, local_output_path):
    """Download classification results from S3."""
    s3 = session.client('s3')
    s3.download_file(s3_output_uri,f"output/{account_id}-CLN-{job_id}/output/output.tar.gz",local_output_path)


def create_jobs(docs_w_metadata:  List[DocumentWithMetadata]):
    job_id_flags={}
    for doc_w_metadata in docs_w_metadata:
        # Extract Text
        text = extract_text_from_pdf(doc_w_metadata.document.path)

        #Upload to S3
        s3_input_key = f'input/{doc_w_metadata.document.path[:-3]}/input.txt'
        upload_to_s3(text, doc_w_metadata.bucket_name, s3_input_key)
        s3_input_uri = f's3://{doc_w_metadata.bucket_name}/{s3_input_key}'
        s3_output_uri = f's3://{doc_w_metadata.bucket_name}/output/'
        
        # Send to document to classify
        job_id_x = start_classification_job(s3_input_uri, s3_output_uri, doc_w_metadata.model_arn)
        doc_w_metadata.job_id = job_id_x
        job_id_flags[job_id_x] = 0
    return job_id_flags