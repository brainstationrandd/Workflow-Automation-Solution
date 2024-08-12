import boto3
import tarfile
import json
import PyPDF2
import os
import time

from dotenv import dotenv_values
config = dotenv_values(".env")
openai_api_key=config['OPENAI_API_KEY'] 
key=config['key']
secret=config['secret']
session_token=config['session_token']
comprehendAITeam=config['comprehendAITeam']


session = boto3.session.Session(
    aws_access_key_id=key,
    aws_secret_access_key=secret,
    aws_session_token=session_token
)

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
        DocumentClassifierArn=model_arn
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
                    return json_data['Classes'][0]

# print_class('result.tar.gz')

def download_classification_results(s3_output_uri, job_id, local_output_path):
    """Download classification results from S3."""
    s3 = session.client('s3')
    # s3_bucket, s3_key = s3_output_uri.replace("s3://", "").split("/", 1)
    # s3_key = f"{s3_key}/{os.path.basename(local_output_path)}"
    # s3.download_file(s3_bucket, s3_key, local_output_path)
    s3.download_file(s3_output_uri,f"output/{job_id}/output/output.tar.gz",local_output_path)

# download_classification_results('s3://cv-trainset/output/','result.json')
s3 = session.client('s3')
# s3.download_file("cv-trainset","output/905418236735-CLN-661e0c91fcdce32172f926f5751f8cec/output/output.tar.gz","result.tar.gz")
# job_id = "905418236735-CLN-661e0c91fcdce32172f926f5751f8cec"


def classify_pdf(pdf_path, bucket_name, model_arn, local_output_path):
    """Extract text from a PDF, upload it to S3, and classify it using Amazon Comprehend."""
    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Upload the text to S3
    s3_input_key = f'input/{pdf_path[:-3]}/input.txt'
    upload_to_s3(text, bucket_name, s3_input_key)
    s3_input_uri = f's3://{bucket_name}/{s3_input_key}'

    # Step 3: Start the classification job
    s3_output_uri = f's3://{bucket_name}/output/'
    job_id = start_classification_job(s3_input_uri, s3_output_uri, model_arn)

    # Step 4: Wait for the job to complete
    while True:
        status = get_classification_job_status(job_id)
        if status in ['COMPLETED', 'FAILED']:
            break
        print(f"Job status: {status}, waiting...")
        time.sleep(30)

    if status == 'COMPLETED':
        # Step 5: Download and return the results
        # local_output_path = 'results.json'
        download_classification_results(s3_output_uri, job_id, local_output_path)
        # with open(local_output_path, 'r') as f:
        #     return f.read()
        category = print_class(local_output_path)
        return category
    else:
        raise Exception("Classification job failed")

# Example usage
pdf_path = 'CV_Main_2_3.pdf'
bucket_name = 'cv-trainset'
# model_arn = 'your_custom_model_arn'
model_arn = 'arn:aws:comprehend:us-east-1:905418236735:document-classifier/cv-classifier-l1/version/1-2'
local_output_path = 'results.json'

# classification_result = classify_pdf(pdf_path, bucket_name, model_arn, local_output_path)
# print(classification_result)

