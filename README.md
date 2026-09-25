# AI-Powered Document Retrieval System

A production-oriented RAG application for document question answering using Hybrid Retrieval, Cross-Encoder Reranking, FastAPI, Streamlit, and Ollama.

## Overview

The system allows users to upload PDF/DOCX documents and ask natural-language questions about their content.

It combines:

- **FAISS** for semantic retrieval
- **BM25** for keyword retrieval
- **Reciprocal Rank Fusion (RRF)** for hybrid ranking
- **Cross-Encoder** for reranking
- **Ollama (Llama 3.2)** for grounded answer generation
- **Conversation Memory** for contextual follow-up questions

## Key Features

- Hybrid Retrieval — FAISS + BM25
- Cross-Encoder Reranking
- Query Rewriting & Multi-Query Retrieval
- Conversation Memory
- Source Citations & Confidence Scoring
- PDF & DOCX Support
- FastAPI REST API
- Streamlit UI
- Docker Support
- GitHub Actions CI

## Architecture

```text
User
  |
  v
Streamlit
  |
  v
FastAPI
  |
  v
Query Router
  |
  v
Query Rewriter
  |
  v
Hybrid Retriever
  |       \
 FAISS    BM25
  \       /
   RRF Fusion
      |
      v
Cross-Encoder
      |
      v
Context Builder
      |
      v
Ollama (Llama 3.2)
      |
      v
Answer + Sources



Tech Stack
Category	Technology
Language	Python 3.11
Backend	FastAPI
Frontend	Streamlit
LLM	Ollama / Llama 3.2
Embeddings	all-MiniLM-L6-v2
Vector Store	FAISS
Keyword Retrieval	BM25
Reranker	Cross-Encoder
Frameworks	LangChain, Sentence Transformers
Document Processing	PyMuPDF, python-docx
CI	GitHub Actions
Deployment	Docker
Quick Start
Prerequisites
Python 3.11
Git
Ollama
1. Clone the Repository
git clone https://github.com/Anu-code4/AI-Powered-Document-Retrieval-System.git
cd AI-Powered-Document-Retrieval-System
2. Create Virtual Environment

Windows

py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

Linux/macOS

python3.11 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Set Up Ollama

Install Ollama and pull the required model:

ollama pull llama3.2

Start Ollama:

ollama serve
Run the Application
1. Start FastAPI

Open a terminal in the project directory:

uvicorn api:app --reload

API:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

2. Start Streamlit

Open a second terminal in the project directory.

Activate the virtual environment if required, then run:

streamlit run frontend/streamlit_app.py

Open the application:

http://localhost:8501

Keep Ollama and FastAPI running while using the Streamlit application.

Prebuilt Retrieval Index

The repository includes the prebuilt retrieval artifacts:

chunks.json
embedded_chunks.json
faiss_index.bin

Rebuilding the vector index is not required to run the included application.

Project Structure
AI-Powered-Document-Retrieval-System/
├── .github/
├── Document/
├── evaluation/
├── frontend/
├── ingestion/
├── llm/
├── memory/
├── metadata/
├── preprocessing/
├── retrievers/
├── utils/
├── api.py
├── app.py
├── config.py
├── query_router.py
├── ragas_evaluator.py
├── chunks.json
├── embedded_chunks.json
├── faiss_index.bin
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
API Endpoints
Method	Endpoint	Purpose
GET	/	Health check
POST	/chat	Question answering
POST	/upload	Document upload and indexing
Evaluation

The project includes a custom evaluation dataset and evaluation pipeline covering retrieval quality, answer relevance, confidence, and source accuracy.

Author

Anukriti Krishna