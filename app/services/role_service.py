from http.client import HTTPException
from app.repository.role_repository import RoleRepository
from utils.logger import logger

def get_role_by_id_service(id: int):
    try:
        role = RoleRepository.get_role_by_id(id)
        return role 
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
def get_role_by_name_service(name: str):
    try:
        role = RoleRepository.get_role_by_name(name)
        return role
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
def create_role_service(name: str):
    try:
        role = RoleRepository.create_role(name)
        return role
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e