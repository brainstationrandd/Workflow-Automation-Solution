from elasticsearch import Elasticsearch


# Initialize Elasticsearch client with scheme
es = Elasticsearch(
    [{'host': 'localhost', 'port': 9300, 'scheme': 'http'}]  # Use 'https' if applicable
)

es.indices.delete(index='cv_data', ignore=[400, 404])


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

# Create the index # RUN IF U WANT TO CREATE NEW INDEX
es.indices.create(index='cv_data', body=index_mapping, ignore=400)