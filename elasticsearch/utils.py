def carregar_queries(dataset):
    print("Carregando queries...")
    queries = {query.query_id: query.text for query in dataset.queries_iter()}
    print(f"Queries carregadas: {len(queries)}")
    return queries


def carregar_qrels(dataset):
    print("Carregando qrels...")
    qrels = {}
    for qrel in dataset.qrels_iter():
        if qrel.relevance > 0:
            qrels.setdefault(qrel.query_id, set()).add(qrel.doc_id)
    print(f"Qrels carregadas: {len(qrels)}")
    return qrels