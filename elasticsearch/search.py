from connection import es
from settings import INDEX_NAME

def search_es(query_text, top_n=20):
    body = {
        "size": top_n,
        "query": {
            "match": {
                "text": query_text
            }
        }
    }
    res = es.search(index=INDEX_NAME, body=body)
    return [(hit["_id"], hit["_score"]) for hit in res["hits"]["hits"]]