from http.client import HTTPException
from app.repository.user_role_repository import UserRoleRepository
from utils.logger import logger

def assign_role_service(user_id:int, role_id: int):
    try: 
        user_role = UserRoleRepository.assign_role(user_id, role_id)
        return user_role
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

