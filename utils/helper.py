from app.config import local_pdf_directory
from utils.logger import logger
import os
import shutil




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