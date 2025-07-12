from tqdm import tqdm

def average_precision(ranked_docs, relevant_docs):
    if not relevant_docs:
        return 0.0

    hits = 0
    sum_precisions = 0
    for i, doc_id in enumerate(ranked_docs):
        if doc_id in relevant_docs:
            hits += 1
            sum_precisions += hits / (i + 1)

    return sum_precisions / len(relevant_docs)


def aval(queries, qrels, search_es):
    print("\nIniciando avaliação MAP...")
    total_ap = 0
    num_queries = 0

    for qid in tqdm(queries.keys(), desc="Avaliação MAP"):
        if qid not in qrels:
            continue

        query_text = queries[qid]
        results = search_es(query_text, top_n=1000)
        ranked_doc_ids = [doc_id for doc_id, _ in results]

        ap = average_precision(ranked_doc_ids, qrels[qid])
        total_ap += ap
        num_queries += 1

    map_score = total_ap / num_queries if num_queries > 0 else 0
    print(f"\nMean Average Precision (MAP) Elasticsearch: {map_score:.4f}")
    print(f"Queries avaliadas: {num_queries}")
    return map_score
