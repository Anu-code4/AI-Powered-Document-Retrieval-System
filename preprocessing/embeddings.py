"""
Generate document embeddings.
"""

import json

from sentence_transformers import SentenceTransformer


def run_embeddings():

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("chunks.json", encoding="utf-8") as f:
        chunks = json.load(f)

    embeddings = model.encode(
        [chunk["text"] for chunk in chunks]
    )

    embedded_chunks = [
        {
            **chunk,
            "embedding": embedding.tolist(),
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]

    with open(
        "embedded_chunks.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            embedded_chunks,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print(
        f"✅ Created embeddings for {len(embedded_chunks)} chunks."
    )


if __name__ == "__main__":
    run_embeddings()