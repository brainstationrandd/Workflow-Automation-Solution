from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from utils.logger import logger
from app.db import engine, SessionLocal, Base, get_db
from app.models.user_role import User_role
from app.services.user_role_service import *
router = APIRouter()

@router.post("/assign-role")
async def assign_role(user_id: int, role_id: int):
    try:
        user_role = await assign_role_service(user_id, role_id)
        return user_role
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
