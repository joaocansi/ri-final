INDEX_NAME = 'cranfield'
INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "english_custom": {
                    "type": "standard",
                    "stopwords": "_english_",
                    "filter": ["lowercase", "porter_stem"]
                }
            },
            "filter": {
                "porter_stem": {
                    "type": "porter_stem"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "doc_id": {"type": "keyword"},
            "text": {
                "type": "text",
                "analyzer": "english_custom"
            },
        }
    }
}