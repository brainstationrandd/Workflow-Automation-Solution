from fastapi import HTTPException
from requests import Session
from utils.logger import logger
from app.models.user import User
from app.db import engine, SessionLocal, Base, get_db
from app.schema.user import UserBase
from app.helpers.hash_password import hash_password
from sqlalchemy.orm import joinedload


class UserRepository:
    @staticmethod
    def get_all_users(db: Session):
        try:
            data = db.query(User)
            return data
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise

    @staticmethod
    def get_user_query(db: Session, skip: int, limit: int):
        try:
            data = db.query(User).offset(skip).limit(limit).all()
            return data
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
    @staticmethod
    async def get_user_by_id(user_id):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    @staticmethod
    async def save_user_query(user: UserBase):
        db = SessionLocal()
        try:
            hashed_password = hash_password(user.password)
            user.password = hashed_password
            db_user = User(**user.dict())  
            db.add(db_user)
            db.commit()
            db.refresh(db_user) 
            return db_user
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    async def delete_user_query(user_id):
        db = SessionLocal()
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user is None:
                raise HTTPException(404, "User not found")
            db.delete(db_user)
            db.commit()
            return db_user
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    async def update_user_query(user_id, user):
        db = SessionLocal()
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user is None:
                raise HTTPException(404, "User not found")
            if(user.name):
                db_user.name = user.name
            if(user.email):
                db_user.email = user.email
            if(user.avatar):
                db_user.avatar = user.avatar
            if(user.password):
                hashed_password = hash_password(user.password)
                db_user.password = hashed_password
            
            db.commit()
            db.refresh(db_user)
            return db_user
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    async def get_user_by_email(db: Session, email: str):
        try:
            user = db.query(User).filter(User.email == email).first()
            return user
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()
    
    
    @staticmethod
    def get_email_by_id(user_id: int):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            return user.email
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()