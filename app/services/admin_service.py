from http.client import HTTPException
from fastapi import HTTPException as FastAPIHTTPException

from sqlalchemy.orm import Session

from app.repository.admin_repository import AdminRepository
# find_chatbot_by_admin, get_admin_query, save_admin_query, delete_admin_query, update_admin_query
from app.schema.admin import AdminBase
from app.helpers.hash_password import check_password
from utils.logger import logger
import os


def find_admins(db: Session, skip: int, limit: int):
    try:
        admins = AdminRepository.get_admin_query(db, skip, limit)
        return admins
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
def get_admin_by_id(id: int):
    try:
        admin = AdminRepository.get_admin_by_id(id)
        return admin
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

def get_admin_by_email(db: Session, email: str):
    try:
        admin = AdminRepository.get_admin_by_email(db, email)
        return admin
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e


async def create_admin_service(admin: AdminBase, avatar):
    try:
        admin_img_directory = "./static/avatar"
        if not os.path.exists(admin_img_directory):
            os.makedirs(admin_img_directory)
        
        if avatar is not None: 
            file_location = f"{admin_img_directory}/{avatar.filename}"
            with open(file_location, "wb") as file:
                file.write(avatar.file.read())
            admin.avatar = file_location.replace("./", "", 1)
        else:
            admin.avatar = None  
        
        db_admin = await AdminRepository.save_admin_query(admin)
        return db_admin
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e



async def delete_admin_service(admin_id):
    try:
        admin = await AdminRepository.delete_admin_query(admin_id)
        return admin
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e


async def update_admin_service(admin_id, admin):
    try:
        admin = await AdminRepository.update_admin_query(admin_id, admin)
        return admin
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
async def update_admin_password_service( admin_id, passwords):
    try:
        if(passwords.new_password != passwords.confirm_password):
            raise FastAPIHTTPException(400, "Passwords do not match")
        
        get_admin = await AdminRepository.get_admin_by_id(admin_id)

        if not get_admin:
            raise FastAPIHTTPException(404, "Admin not found")
        
        isPassCorrect = check_password(passwords.password, get_admin.password)
        print(isPassCorrect)
        if not isPassCorrect:
            raise FastAPIHTTPException(400, "Incorrect password")

        get_admin.password = passwords.new_password
        
        admin = await AdminRepository.update_admin_query(admin_id, get_admin)
        return admin
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
async def update_admin_avater_service(admin_id, avatar):
    try:
        admin_pdf_directory = "./static/avatar"
        if not os.path.exists(admin_pdf_directory):
            os.makedirs(admin_pdf_directory)
        admin = await AdminRepository.get_admin_by_id(admin_id)
        if not admin:
            raise FastAPIHTTPException(404, "Admin not found")
        file_location = f"{admin_pdf_directory}/{avatar.filename}"
        with open(file_location, "wb") as file:
            file.write(avatar.file.read())
        admin.avatar = file_location.replace("./", "", 1)
        admin = await AdminRepository.update_admin_query(admin_id, admin)
        return admin
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
