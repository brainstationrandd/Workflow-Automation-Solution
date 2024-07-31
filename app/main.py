from typing import List
from fastapi import FastAPI, File, HTTPException, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from pathlib import Path


from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger
from app.helpers.helper import http_error_handler
from fastapi.exceptions import RequestValidationError
from app.helpers.custom_exception_handler import validation_exception_handler
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# from app.endpoints import user_controller

sessions = {}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(user_controller.router, prefix="/api/user", tags=["User"])


#Health Checker
@app.get("/")
async def health():
    logger.info("Health check requested")
    return {"Status": "Ok 201"}





# listen the app on port 8000
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000)