from connection import es
from dataset import dataset
from index import index_documents
from utils import carregar_queries, carregar_qrels
from aval import aval
from precision_recall import generate_curve_precision_recall
from search import search_es

index_documents()
queries = carregar_queries(dataset)
qrels = carregar_qrels(dataset)

aval(queries, qrels, search_es)
generate_curve_precision_recall(queries, qrels, search_es)