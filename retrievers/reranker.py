"""
Cross-Encoder Reranker.
"""

from sentence_transformers import CrossEncoder

from utils.logger import setup_logger

setup_logger()

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(
    query: str,
    retrieved_chunks: list,
    top_k: int = 5,
) -> list:

    if not retrieved_chunks:
        return []

    scores = model.predict(
        [(query, chunk["text"]) for chunk in retrieved_chunks]
    )

    for chunk, score in zip(retrieved_chunks, scores):
        chunk["rerank_score"] = float(score)

    results = sorted(
        retrieved_chunks,
        key=lambda chunk: chunk["rerank_score"],
        reverse=True,
    )[:top_k]

    # Reject weak matches
    if results[0]["rerank_score"] < 2.5:
        return []

    confidence = results[0]["rerank_score"]

    for chunk in results:
        chunk["confidence"] = confidence

    return results