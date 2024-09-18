from http.client import HTTPException
from fastapi import HTTPException as FastAPIHTTPException
from sqlalchemy.orm import Session
from app.repository.user_repository import UserRepository
from app.schema.user import UserBase, UserLogin
from app.helpers.hash_password import check_password, check_password_for_login
from utils.logger import logger
import os


def find_users(db: Session, skip: int, limit: int):
    try:
        users = UserRepository.get_user_query(db, skip, limit)
        return users
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

def get_user_by_id_service(id: int):
    try:
        user = UserRepository.get_user_by_id(id)
        return user
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

def get_all_users_service():
    try:
        return UserRepository.get_all_users()
    except Exception as e:
        logger.exception("Error in get_all_users_service")
        raise

def get_user_by_email(db: Session, email: str):
    try:
        user = UserRepository.get_user_by_email(db, email)
        return user
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

async def create_user_service(user: UserBase):
    try:
        db_user = await UserRepository.save_user_query(user)
        return db_user
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e


async def login_user_service(user: UserLogin, db: Session):
    try:
        db_user = await UserRepository.get_user_by_email(db, user.email)
        
        if db_user is None:
            logger.warning(f"Login attempt failed: User not found for email {user.email}")
            raise FastAPIHTTPException(status_code=404, detail="User not found")

        
        if not check_password_for_login(user.password, db_user.password):
            logger.warning(f"Login attempt failed: Incorrect password for user {db_user.email}")
            raise FastAPIHTTPException(status_code=401, detail="Incorrect password")
        
        logger.info(f"User logged in successfully: {db_user.email}")
        return db_user
    
    except FastAPIHTTPException as e:
        logger.error(f"HTTP exception during login: {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise FastAPIHTTPException(status_code=500, detail="Internal server error")


async def delete_user_service(user_id):
    try:
        user = await UserRepository.delete_user_query(user_id)
        return user
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e


async def update_user_service(user_id, user):
    try:
        user = await UserRepository.update_user_query(user_id, user)
        return user
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
async def update_user_password( user_id, passwords):
    try:
        if(passwords.new_password != passwords.confirm_password):
            raise FastAPIHTTPException(400, "Passwords do not match")
        
        get_user = await UserRepository.get_user_by_id(user_id)

        if not get_user:
            raise FastAPIHTTPException(404, "User not found")
        
        isPassCorrect = check_password(passwords.password, get_user.password)
        print(isPassCorrect)
        if not isPassCorrect:
            raise FastAPIHTTPException(400, "Incorrect password")

        get_user.password = passwords.new_password
        
        user = await UserRepository.update_user_query(user_id, get_user)
        return user
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
async def update_user_avater(user_id, avatar):
    try:
        user_img_directory = "./static/avatar"
        if not os.path.exists(user_img_directory):
            os.makedirs(user_img_directory)
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise FastAPIHTTPException(404, "User not found")
        file_location = f"{user_img_directory}/{avatar.filename}"
        with open(file_location, "wb") as file:
            file.write(avatar.file.read())
        user.avatar = file_location.replace("./", "", 1)
        user = await UserRepository.update_user_query(user_id, user)
        return user
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
