"""
FastAPI entry point for AI-Powered Document Retrieval System
"""

import logging
import shutil
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app import get_answer, stream_response
from ingestion.file_tracker import update_metadata
from preprocessing.chunking import run_chunking
from preprocessing.embeddings import run_embeddings
from preprocessing.vector_store import build_vector_store


logger = logging.getLogger(__name__)
DOCUMENT_FOLDER = Path("Document")


app = FastAPI(
    title="AI-Powered Document Retrieval System",
    version="1.0.0",
    description="Production RAG API",
)


# ==========================================================
# Models
# ==========================================================

class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    document: str
    chunks: list[int]


class ChatResponse(BaseModel):
    answer: str
    confidence: float | None = None
    sources: list[Source] = Field(default_factory=list)


# ==========================================================
# Helper
# ==========================================================

def rebuild_index():
    """Rebuild retrieval index."""

    logger.info("Rebuilding search index...")

    run_chunking()
    run_embeddings()
    build_vector_store()
    update_metadata()

    logger.info("Index rebuilt successfully.")


# ==========================================================
# Routes
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "AI-Powered Document Retrieval System API is running."
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = get_answer(request.question)

    return ChatResponse(
        answer=result["answer"],
        confidence=result["confidence"],
        sources=result["sources"],
    )


@app.post("/upload")
async def upload_documents(
    files: Annotated[list[UploadFile], File(...)],
):
    DOCUMENT_FOLDER.mkdir(exist_ok=True)

    uploaded_files = []

    try:
        for file in files:
            with (DOCUMENT_FOLDER / file.filename).open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            uploaded_files.append(file.filename)

        rebuild_index()

    except Exception as e:
        logger.exception("Document indexing failed.")

        raise HTTPException(
            status_code=500,
            detail=f"Document indexing failed: {e}",
        )

    return {
        "message": f"{len(uploaded_files)} file(s) uploaded and indexed successfully.",
        "uploaded_files": uploaded_files,
    }


@app.get("/documents")
def list_documents():
    DOCUMENT_FOLDER.mkdir(exist_ok=True)

    return [
        {
            "filename": file.name,
            "type": file.suffix.replace(".", "").upper(),
            "size_kb": round(file.stat().st_size / 1024, 2),
        }
        for file in sorted(DOCUMENT_FOLDER.iterdir())
        if file.is_file()
    ]


@app.delete("/documents/{filename}")
def delete_document(filename: str):
    file_path = DOCUMENT_FOLDER / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    try:
        file_path.unlink()
        rebuild_index()

        return {
            "message": f"{filename} deleted successfully."
        }

    except Exception as e:
        logger.exception("Failed to delete document.")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/stream")
def stream(request: ChatRequest):
    return StreamingResponse(
        stream_response(request.question),
        media_type="text/plain",
    )