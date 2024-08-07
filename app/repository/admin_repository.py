from requests import Session
from fastapi import HTTPException
from app.models.admin import Admin
from utils.logger import logger
from app.db import SessionLocal
from app.helpers.hash_password import hash_password


class AdminRepository:
    @staticmethod
    def get_all_admins(db: Session):
        try:
            data = db.query(Admin)
            return data
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise

    @staticmethod
    def get_admin_query(db: Session, skip: int, limit: int):
        try:
            data = db.query(Admin).offset(skip).limit(limit).all()
            return data
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
    @staticmethod
    async def get_admin_by_id(admin_id):
        db = SessionLocal()
        try:
            admin = db.query(Admin).filter(Admin.id == admin_id).first()
            if not admin:
                raise HTTPException(status_code=404, detail="Admin not found")
            return admin
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def save_admin_query(admin: AdminBase):
        db = SessionLocal()
        try:
            hashed_password = hash_password(admin.password)
            admin.password = hashed_password
            db_admin = Admin(**admin.dict())  
            db.add(db_admin)
            db.commit()
            db.refresh(db_admin) 
            return db_admin
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    async def delete_admin_query(admin_id):
        db = SessionLocal()
        try:
            db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
            if db_admin is None:
                raise HTTPException(404, "Admin not found")
            db.delete(db_admin)
            db.commit()
            return db_admin
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    async def update_admin_query(admin_id, admin):
        db = SessionLocal()
        try:
            db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
            if db_admin is None:
                raise HTTPException(404, "Admin not found")
            if(admin.name):
                db_admin.name = admin.name
            if(admin.phone):
                db_admin.phone = admin.phone
            if(admin.email):
                db_admin.email = admin.email
            if(admin.avatar):
                db_admin.avatar = admin.avatar
            # if(admin.password):
            #     hashed_password = hash_password(admin.password)
            #     db_admin.password = hashed_password
            
            db.commit()
            db.refresh(db_admin)
            return db_admin
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    async def get_admin_by_email(db: Session, email: str):
        try:
            admin = db.query(Admin).filter(Admin.email == email).first()
            return admin
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()