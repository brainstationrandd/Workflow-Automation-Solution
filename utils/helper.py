from app.config import local_pdf_directory
from utils.logger import logger
import os
import shutil
from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import BedrockChat
from langchain_community.embeddings import BedrockEmbeddings


config = dotenv_values(".env")
openai_api_key=config['OPENAI_API_KEY'] 

model_gpt_4o_mini = ChatOpenAI(
    model_name="gpt-4o-mini",
    streaming=True,
    temperature=0.5, 
    api_key=openai_api_key
)



def custom_response_handler(status_code: int, message: str, data=None):
    if data is None:
        return {
            "status_code": status_code,
            "message": message,
        }
    else:
        return {
            "status_code": status_code,
            "message": message,
            "data": data,
        }
    

def move_file_classified_directory(file_name, category, old_directory = local_pdf_directory):
    try:
        classified_directory = os.path.join(old_directory, category)
        os.makedirs(classified_directory, exist_ok = True)
        classified_file = os.path.join(classified_directory, file_name)
        existing_file = os.path.join(old_directory, file_name) 
        shutil.move(existing_file, classified_file)
        logger.info(f"{file_name} moved from {old_directory} to {classified_directory}" )
        return classified_file
    except Exception as e:
        logger.info(f"Exception {e} occured while moving {file_name} from {old_directory} to {classified_directory}")