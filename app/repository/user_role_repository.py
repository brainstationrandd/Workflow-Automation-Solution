from app.db import engine, SessionLocal, Base, get_db
from fastapi import HTTPException
from app.models.user_role import User_role
from utils.logger import logger


class UserRoleRepository:
    @staticmethod
    async def assign_role(user_id: int, role_id: int):
        db = SessionLocal()
        try:
            new_user_role = User_role(user_id = user_id, role_id = role_id)
            db.add(new_user_role)
            db.commit()
            db.refresh(new_user_role)
            return new_user_role
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
