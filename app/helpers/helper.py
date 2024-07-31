from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
import secrets
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
# import random

async def http_error_handler(request: Request, exc: HTTPException):
    print(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )

def custom_response_handler(status_code: int, message: str, data=None):
    if data is None:
        return {
            "status_code": status_code,
            "message": message,
        }
    else:
        return {
            "status_code": status_code,
            "message": message,
            "data": data,
        }
