from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from utils.logger import logger

router = APIRouter()

