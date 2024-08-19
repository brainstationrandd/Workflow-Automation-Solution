from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from app.db import get_db
from app.schema.role import *
from app.helpers.custom_exception_handler import *
from utils.helper import custom_response_handler
from utils.logger import logger
from app.services.role_service import *

router = APIRouter()



@router.get("/{role_id}", response_model=RoleBase)
async def get_role_by_id(role_id: int):
    try:
        role = await get_role_by_id_service(role_id)
        return role
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.post("/role-name/", response_model=RoleBase)
async def get_role_by_name(role_name: str):
    try:
        role = await get_role_by_name_service(role_name)
        return role
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.post("/create-role/", response_model=RoleBase)
async def create_role(name: str):
    try:
        role = await create_role_service(name)
        return role
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


