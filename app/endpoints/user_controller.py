from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from app.db import get_db
from app.schema.user import *
from app.services.user_service import *
from app.helpers.custom_exception_handler import *
from utils.helper import custom_response_handler
from app.models.user import User

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
    
@router.get("/paginated")
async def get_users_with_pagination(offset: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    """
    Get users with pagination.
    - offset: The number of items to skip before starting to collect the result set.
    - limit: The number of items to return.
    """
    try:
        users = find_users(db, offset, limit)  # Removed await here since it's not async
        return custom_response_handler(200, "Users retrieved successfully", users)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail="An error occurred: {}".format(str(e)))

    


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

@router.get("/users/search")
async def find_users_by_name(
    name: str ,# Name is required, with at least one character
    db: Session = Depends(get_db)
):
    """
    Find users by name prefix (case-insensitive).
    - name: The prefix of the user name to search for.
    """
    try:
        users = await find_users_by_name_service(db, name)
        return custom_response_handler(200, "Users retrieved successfully", users)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="An error occurred while searching for users.")