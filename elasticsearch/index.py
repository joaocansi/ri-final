from dataset import dataset
from connection import es
from tqdm import tqdm
from settings import INDEX_NAME

def index_documents():
    print("Indexando documentos...")
    batch = []
    doc_count = 0
    for i, doc in tqdm(enumerate(dataset.docs_iter()), total=dataset.docs_count()):
        batch.append({"index": {"_index": INDEX_NAME, "_id": doc.doc_id}})
        batch.append({"doc_id": doc.doc_id, "text": doc.title + ' ' + doc.text})
        doc_count += 1
        if len(batch) >= 1000 * 2:
            es.bulk(body=batch)
            batch = []
    if batch:
        es.bulk(body=batch)
    print(f"Indexação concluída. {doc_count} documentos indexados.")
    es.indices.refresh(index=INDEX_NAME)