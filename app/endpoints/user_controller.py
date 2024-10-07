from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from app.db import get_db
from app.schema.user import *
from app.services.user_service import *
from app.helpers.custom_exception_handler import *
from utils.helper import custom_response_handler

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserBase):
    try:
        created_user = await create_user_service(user)
        return custom_response_handler(201, "User created successfully", created_user)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e


@router.post("/login", response_model=UserResponse)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        logged_in_user = await login_user_service(user, db)
        return custom_response_handler(200, "User logged in successfully", logged_in_user)
    except HTTPException as e:
        raise e


@router.get("/")
async def get_all_users():
    try:
        users = await get_all_users_service()
        return custom_response_handler(200, "Users retrieved successfully", users)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    try:
        user = await get_user_by_id_service(user_id)
        return custom_response_handler(200, "User retrieved successfully", user)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user: UpdateUser, user_id: int):
    try:
        user = await update_user_service(user_id, user)
        return custom_response_handler(200, "User updated successfully", user)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    try:
        await delete_user_service(user_id)
        return custom_response_handler(200, "User deleted successfully")
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
