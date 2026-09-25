"""
Semantic Retriever using FAISS.
"""

import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

from config import FAISS_DISTANCE_THRESHOLD


model = SentenceTransformer("all-MiniLM-L6-v2")

embedded_chunks = []
index = None


def load_index():

    global embedded_chunks, index

    if index:
        return

    chunk_file = Path("embedded_chunks.json")
    index_file = Path("faiss_index.bin")

    if not chunk_file.exists() or not index_file.exists():
        return

    with open(chunk_file, encoding="utf-8") as f:
        embedded_chunks = json.load(f)

    index = faiss.read_index(str(index_file))


def retrieve_faiss(
    query: str,
    top_k: int = 3,
    threshold: float = FAISS_DISTANCE_THRESHOLD,
    filters: dict | None = None,
):

    load_index()

    if not index:
        return []

    distances, indices = index.search(
        model.encode([query]),
        top_k,
    )

    results = []

    for rank, (distance, idx) in enumerate(
        zip(distances[0], indices[0]), 1
    ):

        if idx == -1 or (
            threshold is not None
            and distance > threshold
        ):
            continue

        chunk = embedded_chunks[idx]

        if filters and (
            (
                filters.get("file_type")
                and chunk["file_type"] != filters["file_type"]
            )
            or (
                filters.get("source")
                and chunk["source"].lower()
                != filters["source"].lower()
            )
        ):
            continue

        results.append(
            {
                "id": chunk["id"],
                "index": idx,
                "rank": rank,
                "retriever": "faiss",
                "distance": float(distance),
                "source": chunk["source"],
                "file_type": chunk["file_type"],
                "text": chunk["text"],
            }
        )

    return results