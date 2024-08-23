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


def move_file_to_classified_directory(category, old_file):
    try:
        # Extract the directory path and file name from the old_file path
        old_directory = os.path.dirname(old_file)
        file_name = os.path.basename(old_file)
        
        # Create the new directory path by adding the category
        new_directory = os.path.join(old_directory, category)
        
        # Ensure the new directory exists
        os.makedirs(new_directory, exist_ok=True)
        
        # Create the new file path
        new_file_path = os.path.join(new_directory, file_name)
        
        # Move the file to the new directory
        shutil.move(old_file, new_file_path)
        
        logger.info(f"{file_name} moved from {old_directory} to {new_directory}")

        return new_file_path
    except Exception as e:
        logger.info(f"Exception {e} occured while moving {old_file}")