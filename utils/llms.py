from dotenv import dotenv_values
import boto3
from langchain_aws import ChatBedrock
from app.config import *


session = boto3.session.Session(
    aws_access_key_id=key,
    aws_secret_access_key=secret,
    aws_session_token=session_token,
    region_name="us-east-1"
)

bedrock = session.client('bedrock-runtime',region_name="us-east-1")

model_mistral= ChatBedrock(
    model_id="mistral.mistral-7b-instruct-v0:2",
    model_kwargs=dict(temperature=0.05),
    client=bedrock,

)

model_mistral_large= ChatBedrock(
    model_id="mistral.mistral-large-2402-v1:0",
    model_kwargs=dict(temperature=0.05),
    client=bedrock,

)

model_amazon= ChatBedrock(
    model_id="amazon.titan-text-express-v1",
    model_kwargs=dict(temperature=0.05),
    client=bedrock,

)

model_amazon_premier= ChatBedrock(
    model_id="amazon.titan-text-premier-v1:0",
    model_kwargs=dict(temperature=0.05),
    client=bedrock,

)

