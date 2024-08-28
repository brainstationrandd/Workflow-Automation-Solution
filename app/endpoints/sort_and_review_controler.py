from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os
import json
import datetime
from prompt.review_sort_prompt import sort_review_chain
from langchain_community.document_loaders import PyPDFLoader
router = APIRouter()

# Assuming sort_json_data_based_on_score_desc is a function that sorts JSON data based on score
def sort_json_data_based_on_score_desc(data):
    return sorted(data, key=lambda x: x['score'], reverse=True)

# Define a Pydantic model for the request
class ProcessCVRequest(BaseModel):
    folder_path: str
    job_desc: str

# Define a Pydantic model for the response
class CVData(BaseModel):
    id: str
    score: float
    remarks: List[str]
    created_at: str

@router.post("/process-cvs/", response_model=List[CVData])
async def process_cvs(request: ProcessCVRequest):
    folder_path = request.folder_path
    job_desc = request.job_desc

    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=400, detail="Invalid folder path")

    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
    json_data = []
    batch_size = 10  # Adjust batch size as needed

    for i in range(0, len(files), batch_size):
        batch_text = []
        batch_files = files[i:i+batch_size]
        batch_ids = []

        for file in batch_files:
            loader = PyPDFLoader(file)
            docs = loader.load()
            page_content = "\n\n".join(doc.page_content for doc in docs)
            batch_text.append({"cv_text": page_content, "job_desc": job_desc})
            batch_ids.append(file)  # Append the path of the file

        # Call the batch method without await if it is not asynchronous
        ans = sort_review_chain.batch(batch_text)

        for j in range(len(ans)):
            convert_ans = json.loads(ans[j])
            convert_ans['id'] = batch_ids[j]
            convert_ans['created_at'] = datetime.datetime.now().isoformat()
            json_data.append(convert_ans)

    sorted_data = sort_json_data_based_on_score_desc(json_data)

    return sorted_data