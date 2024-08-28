from prompt.cv_info_extract import chain
from utils.logger import logger
import datetime
from langchain_community.document_loaders import PyPDFLoader
import os,json

from utils.helper import es

index_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "email": {"type": "keyword"},  # Case-sensitive
            "phone": {"type": "keyword", "normalizer": "lowercase_normalizer"},
            "keywords": {"type": "keyword", "normalizer": "lowercase_normalizer"},
            "experience": {"type": "integer"},
            "education": {"type": "text"},
            "skills": {"type": "keyword", "normalizer": "lowercase_normalizer"},
            "location": {"type": "text"},
            "created_at": {"type": "date"}
        }
    },
    "settings": {
        "analysis": {
            "normalizer": {
                "lowercase_normalizer": {
                    "type": "custom",
                    "filter": ["lowercase"]
                }
            }
        }
    }
}


if not es.indices.exists(index='cv_data'):
    es.indices.create(index='cv_data', body=index_mapping, ignore=400)
    
if es.ping():
    logger.info("Connected to ElasticSearch")
else:
    logger.error("Could not connect to ElasticSearch")    

def add_cv_file_to_index(filepath):
    try:
            loader=PyPDFLoader(filepath)
            docs=loader.load()
            page_content="\n\n".join(doc.page_content for doc in docs)
            cv_data = chain.invoke({"cv_text": page_content})
            converted_ans=json.loads(cv_data)
            converted_ans['id'] = os.path.splitext(os.path.basename(filepath))[0]
            converted_ans['created_at'] = datetime.datetime.now().isoformat()
           
            es.index(index='cv_data', id=converted_ans['id'], body=converted_ans)
            logger.info(f"CV file {filepath} added to index")
            
    except Exception as e:
        logger.error(f"Exception {e} occured while adding CV file  to index")
        