import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd

def interpolated_precision_recall(ranked_docs, relevant_docs, recall_levels):
    """Calcula a precisão interpolada nos níveis de recall especificados para uma única consulta."""
    if not relevant_docs:
        return [0.0] * len(recall_levels)

    precisions_at_recall = []
    hits = 0

    for i, doc_id in enumerate(ranked_docs):
        if doc_id in relevant_docs:
            hits += 1
            precision = hits / (i + 1)
            recall = hits / len(relevant_docs)
            precisions_at_recall.append((precision, recall))

    # Adiciona extremos para interpolação
    precisions_at_recall.insert(0, (1.0, 0.0))
    if precisions_at_recall[-1][1] < 1.0:
        precisions_at_recall.append((0.0, 1.0))

    # Interpolação nos níveis de recall
    interpolated = []
    for r in recall_levels:
        precs = [p for p, rec in precisions_at_recall if rec >= r]
        interpolated.append(max(precs) if precs else 0.0)

    return interpolated


def generate_curve_precision_recall(queries, qrels, search_es):
    """Gera curva interpolada de precisão-recall para várias queries."""
    print("\nCalculando curva precision-recall...")
    recall_points = [i / 10 for i in range(11)]  # 0.0, 0.1, ..., 1.0
    precisions_all = []

    for qid in tqdm(queries.keys(), desc="Precision-Recall"):
        if qid not in qrels:
            continue

        query_text = queries[qid]
        results = search_es(query_text, top_n=1000)

        if not results:
            continue

        ranked_doc_ids = [doc_id for doc_id, _ in results]
        relevant_doc_ids = qrels[qid]

        ip = interpolated_precision_recall(ranked_doc_ids, relevant_doc_ids, recall_points)
        precisions_all.append(ip)

    if precisions_all:
        avg_precisions = np.mean(precisions_all, axis=0)

        # Plot da curva interpolada
        plt.figure(figsize=(10, 6))
        plt.plot(recall_points, avg_precisions, marker='o', linestyle='-', label="Elasticsearch")
        plt.xlabel("Recall")
        plt.ylabel("Interpolated Precision")
        plt.title("11-Point Interpolated Precision-Recall Curve - Elasticsearch")
        plt.xticks(recall_points)
        plt.ylim([0, 1.05])
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("precision_recall_curve.png", dpi=300)

        print(f"Precision média no recall 0.0: {avg_precisions[0]:.4f}")

        f1_scores = []
        for p, r in zip(avg_precisions, recall_points):
            f1 = 0.0 if (p + r == 0) else 2 * p * r / (p + r)
            f1_scores.append(f1)

        avg_f1 = np.mean(f1_scores)
        print(f"F1-score médio (11 pontos): {avg_f1:.4f}")
        print(f"Precisão interpolada média nos 11 pontos:\n{avg_precisions}")

        avg_metrics_df = pd.DataFrame({
            'interpolated_recalls_at_levels': recall_points,
            'interpolated_precisions_at_levels': avg_precisions,
            'interpolated_f1_at_levels': f1_scores,
        })
        avg_metrics_df.to_csv('./../avg_elasticsearch_metrics.csv', index=False)
        print("Métricas médias salvas em avg_elasticsearch_metrics.csv")
    else:
        print("Nenhuma query foi avaliada para precision-recall!")
