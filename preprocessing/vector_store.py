"""
Build FAISS Vector Store.
"""

import json

import faiss
import numpy as np


def build_vector_store():

    with open("embedded_chunks.json", encoding="utf-8") as f:
        embeddings = np.array(
            [
                chunk["embedding"]
                for chunk in json.load(f)
            ],
            dtype="float32",
        )

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(embeddings)
    faiss.write_index(index, "faiss_index.bin")

    print(
        f"✅ FAISS index created with {index.ntotal} vectors."
    )


if __name__ == "__main__":
    build_vector_store()