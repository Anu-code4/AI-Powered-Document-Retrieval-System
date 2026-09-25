"""
Hybrid Retriever
"""

import logging

import utils.logger
from config import MAX_RERANK_CANDIDATES, RRF_K, TOP_K
from llm.multi_query import generate_multi_queries

from .bm25_retriever import retrieve_bm25
from .metadata_filter import extract_metadata_filter
from .reranker import rerank
from .retriever import retrieve_faiss

utils.logger.setup_logger()
logger = logging.getLogger(__name__)


def fuse_results(fused_results: dict, results: list):
    """Merge results using Reciprocal Rank Fusion."""

    for result in results:
        chunk = fused_results.setdefault(
            result["id"],
            {**result, "rrf_score": 0},
        )

        chunk["rrf_score"] += 1 / (RRF_K + result["rank"])

        key = "distance" if result["retriever"] == "faiss" else "score"
        chunk[key] = result.get(key)


def hybrid_retriever(
    query: str,
    top_k: int = TOP_K,
) -> list:
    """Hybrid retrieval using FAISS + BM25 + RRF."""

    filters = extract_metadata_filter(query)
    fused_results = {}

    for q in generate_multi_queries(query):

        results = retrieve_faiss(
            query=q,
            top_k=20,
            filters=filters,
        ) + retrieve_bm25(
            query=q,
            top_k=20,
            filters=filters,
        )

        fuse_results(fused_results, results)

    return rerank(
        query=query,
        retrieved_chunks=sorted(
            fused_results.values(),
            key=lambda x: x["rrf_score"],
            reverse=True,
        )[:MAX_RERANK_CANDIDATES],
        top_k=top_k,
    )


if __name__ == "__main__":

    query = input("Enter your query: ")

    for chunk in hybrid_retriever(query):

        print("-" * 60)

        for key in (
            "rank",
            "index",
            "source",
            "file_type",
            "retriever",
        ):
            print(f"{key.title():10}: {chunk[key]}")

        print(f"RRF Score : {chunk['rrf_score']:.6f}")

        if "distance" in chunk:
            print(f"Distance  : {chunk['distance']:.4f}")

        if "score" in chunk:
            print(f"BM25 Score: {chunk['score']:.4f}")

        print(f"\n{chunk['text']}")
        print("-" * 60)