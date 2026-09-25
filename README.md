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