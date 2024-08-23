from prompt.cv_info_extract import chain
from utils.logger import logger
import datetime
from langchain_community.document_loaders import PyPDFLoader
import os,json

from elasticsearch import Elasticsearch


# Initialize Elasticsearch client with scheme
es = Elasticsearch(
    [{'host': 'localhost', 'port': 9300, 'scheme': 'http'}]  # Use 'https' if applicable
)



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
        