from fastapi import HTTPException
from utils.logger import logger
from app.db import engine, SessionLocal, Base, get_db