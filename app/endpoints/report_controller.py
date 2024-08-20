from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from app.db import get_db
from app.schema.report import *
from app.services.report_service import *
from utils.helper import custom_response_handler

router = APIRouter()

# @router.post("/request-report/")
# async def request_report(query: ReportBase):
#     try:
#         report = await get_report_service(query)
