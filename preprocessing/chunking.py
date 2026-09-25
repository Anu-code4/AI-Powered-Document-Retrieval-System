"""
Document Loader and Chunking.
"""

import json
from pathlib import Path

import fitz
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingestion.file_tracker import detect_changes


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


def extract_text(file):

    if file.suffix == ".docx":
        return "\n".join(
            p.text for p in Document(file).paragraphs
        )

    with fitz.open(file) as pdf:
        return "\n".join(
            page.get_text() for page in pdf
        )


def load_documents(files):

    return [
        {
            "source": file.name,
            "file_type": file.suffix,
            "text": extract_text(file),
        }
        for file in map(Path, files)
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def run_chunking():

    new_files, modified_files, _ = detect_changes()

    documents = load_documents(new_files + modified_files)

    if not documents:
        print("✅ No new or modified documents found.")
        return

    chunk_data = []
    chunk_id = 0

    for doc in documents:
        for chunk in splitter.split_text(doc["text"]):
            chunk_data.append(
                {
                    "id": chunk_id,
                    "source": doc["source"],
                    "file_type": doc["file_type"],
                    "text": chunk,
                }
            )
            chunk_id += 1

    with open(
        "chunks.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            chunk_data,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print(
        f"✅ {len(chunk_data)} chunks created from "
        f"{len(documents)} document(s)."
    )


if __name__ == "__main__":
    run_chunking()