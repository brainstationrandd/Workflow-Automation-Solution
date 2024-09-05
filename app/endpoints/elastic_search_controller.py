from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.user_role_service import *
router = APIRouter()
# from utils.helper import es

from elasticsearch import Elasticsearch


es = Elasticsearch(
    [{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}]  # Use 'https' if applicable
)


# @router.get("/search")
# async def search_cv(
#     name: Optional[str] = None,
#     email: Optional[str] = None,
#     phone: Optional[str] = None,
#     keywords: Optional[List[str]] = Query(None),
#     experience: Optional[int] = None,
#     education: Optional[List[str]] = Query(None),
#     skills: Optional[List[str]] = Query(None),
#     location: Optional[str] = None
# ):
#     query_clauses = []
    
#     #todo if else fix

#     # Construct the query based on provided fields
#     if name:
#         query_clauses.append({"match": {"name": name}})
#     if email:
#         query_clauses.append({"match": {"email": email}})
#     if phone:
#         query_clauses.append({"match": {"phone": phone}})
#     if keywords:
#         query_clauses.append({"terms": {"keywords": keywords}})
#     if experience:
#         query_clauses.append({"range": {"experience": {"gte": experience}}})
#     if education:
#         query_clauses.append({"terms": {"education": education}})
#     if skills:
#         query_clauses.append({"terms": {"skills": skills}})
#     if location:
#         query_clauses.append({"match": {"location": location}})

#     query = {
#         "bool": {
#             "must": query_clauses
#         }
#     }

#     # Perform the search
#     response = es.search(index='cv_data', body={"query": query})

#     # Return the search results
#     return {"results": [hit['_source'] for hit in response['hits']['hits']]}

# @router.websocket("/search")
# async def websocket_search(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_json()
#             query_clauses = []

#             if "name" in data and data["name"]:
#                 query_clauses.append({"match": {"name": data["name"]}})
#             if "email" in data and data["email"]:
#                 query_clauses.append({"match": {"email": data["email"]}})
#             if "phone" in data and data["phone"]:
#                 query_clauses.append({"match": {"phone": data["phone"]}})
#             if "keywords" in data and data["keywords"]:
#                 query_clauses.append({
#                     "bool": {
#                         "should": [{"match": {"keywords": keyword}} for keyword in data["keywords"]],
#                         "minimum_should_match": 1
#                     }
#                 })
#             if "experience" in data and data["experience"] is not None:
#                 query_clauses.append({"range": {"experience": {"gte": data["experience"]}}})
#             if "education" in data and data["education"]:
#                 query_clauses.append({
#                     "bool": {
#                         "should": [{"match": {"education": edu}} for edu in data["education"]],
#                         "minimum_should_match": 1
#                     }
#                 })
#             if "skills" in data and data["skills"]:
#                 query_clauses.append({
#                     "bool": {
#                         "should": [{"match": {"skills": skill}} for skill in data["skills"]],
#                         "minimum_should_match": 1
#                     }
#                 })
#             if "location" in data and data["location"]:
#                 query_clauses.append({"match": {"location": data["location"]}})

#             query = {
#                 "bool": {
#                     "must": query_clauses
#                 }
#             }

#             response = es.search(index='cv_data', body={"query": query})
#             results = [hit['_source'] for hit in response['hits']['hits']]
#             await websocket.send_json({"results": results})

#     except WebSocketDisconnect:
#         print("Client disconnected")

@router.websocket("/search")
async def websocket_search(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            query_clauses = []

            if "name" in data and data["name"]:
                query_clauses.append({"prefix": {"name": data["name"]}})
            if "email" in data and data["email"]:
                query_clauses.append({"prefix": {"email": data["email"]}})
            if "phone" in data and data["phone"]:
                query_clauses.append({"prefix": {"phone": data["phone"]}})
            if "keywords" in data and data["keywords"]:
                query_clauses.append({
                    "bool": {
                        "should": [{"match": {"keywords": keyword}} for keyword in data["keywords"]],
                        "minimum_should_match": 1
                    }
                })
            if "experience" in data and data["experience"] is not None:
                query_clauses.append({"range": {"experience": {"gte": data["experience"]}}})
            if "education" in data and data["education"]:
                query_clauses.append({
                    "bool": {
                        "should": [{"match": {"education": edu}} for edu in data["education"]],
                        "minimum_should_match": 1
                    }
                })
            if "skills" in data and data["skills"]:
                query_clauses.append({
                    "bool": {
                        "should": [{"match": {"skills": skill}} for skill in data["skills"]],
                        "minimum_should_match": 1
                    }
                })
            if "location" in data and data["location"]:
                query_clauses.append({"prefix": {"location": data["location"]}})

            query = {
                "bool": {
                    "must": query_clauses
                }
            }

            response = es.search(index='cv_data', body={"query": query})
            results = [hit['_source'] for hit in response['hits']['hits']]
            await websocket.send_json({"results": results})

    except WebSocketDisconnect:
        print("Client disconnected")