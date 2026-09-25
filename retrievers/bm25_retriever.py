"""
BM25 Retriever.
"""

import json
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

from config import TOP_K


embedded_chunks = []
bm25 = None


def load_bm25():

    global embedded_chunks, bm25

    if bm25:
        return

    file = Path("embedded_chunks.json")

    if not file.exists():
        return

    embedded_chunks = json.loads(
        file.read_text(encoding="utf-8")
    )

    bm25 = BM25Okapi(
        [
            chunk["text"].lower().split()
            for chunk in embedded_chunks
        ]
    )


def retrieve_bm25(
    query: str,
    top_k: int = TOP_K,
    filters: dict | None = None,
):

    load_bm25()

    if not bm25:
        return []

    scores = bm25.get_scores(query.lower().split())

    return [
        {
            "id": chunk["id"],
            "index": int(idx),
            "rank": rank,
            "retriever": "bm25",
            "score": float(scores[idx]),
            "source": chunk["source"],
            "file_type": chunk["file_type"],
            "text": chunk["text"],
        }
        for rank, idx in enumerate(
            np.argsort(scores)[::-1][:top_k], 1
        )
        for chunk in [embedded_chunks[idx]]
        if not (
            filters
            and (
                filters.get("file_type")
                and chunk["file_type"] != filters["file_type"]
                or filters.get("source")
                and chunk["source"].lower()
                != filters["source"].lower()
            )
        )
    ]


if __name__ == "__main__":

    for chunk in retrieve_bm25(input("Enter your query: ")):

        print("-" * 60)
        print(f"Rank     : {chunk['rank']}")
        print(f"Document : {chunk['source']}")
        print(f"Score    : {chunk['score']:.4f}")
        print(chunk["text"])