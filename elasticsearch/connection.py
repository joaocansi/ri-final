from elasticsearch import Elasticsearch 
from settings import INDEX_NAME, INDEX_SETTINGS

def __connect():
    es = Elasticsearch(
        "http://localhost:9200",
        request_timeout=60,
        max_retries=10,
        retry_on_timeout=True)
    
    if not es.ping():
        return None
    
    if es.indices.exists(index=INDEX_NAME):
        print(f"Deletando índice {INDEX_NAME}...")
        es.indices.delete(index=INDEX_NAME)

    print(f"Criando índice {INDEX_NAME}...")
    es.indices.create(index=INDEX_NAME, body=INDEX_SETTINGS)
    return es

es = __connect()