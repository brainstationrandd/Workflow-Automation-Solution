from app.db import engine, SessionLocal, Base, get_db
from fastapi import HTTPException
from app.models.role import Role
from app.schema.role import *
from utils.logger import logger


class RoleRepository:
    @staticmethod
    async def get_role_by_id(role_id: int):
        db = SessionLocal()
        try:
            role = db.query(Role).filter(Role.id == role_id).first()
            if not role:
                raise HTTPException(status_code=404, detail="Role not found")
            return role
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    @staticmethod
    async def get_role_by_name(role: str):
        db = SessionLocal()
        try:
            role_name = db.query(Role).filter(Role.name == role).first()
            if not role_name:
                raise HTTPException(status_code=404, detail="Role not found")
            return role_name
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    @staticmethod
    async def create_role(name: str):
        db = SessionLocal()
        try :
            new_role = Role(name=name)
            db.add(new_role)
            db.commit()
            db.refresh(new_role)
            return new_role
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

        