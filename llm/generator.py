"""
LLM response generation.
"""

from ollama import chat

from config import MODEL_NAME, TEMPERATURE
from query_router import QueryType
from .prompts import SYSTEM_PROMPT


def build_prompt(question, chunks, history, query_type):

    context = (
        "\n\n".join(chunk["text"] for chunk in chunks)
        if query_type == QueryType.DOCUMENT
        else ""
    )

    history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in (history or [])
    )

    return f"""
{SYSTEM_PROMPT}

Conversation History:
{history}

Retrieved Context:
{context}

Query Type:
{query_type.value}

User Question:
{question}
""".strip()


def ollama_chat(prompt, stream=False):
    return chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": TEMPERATURE},
        stream=stream,
    )


def generate_answer(
    question,
    retrieved_chunks,
    conversation_history=None,
    query_type=QueryType.DOCUMENT,
):

    if query_type == QueryType.CHAT:
        return {
            "answer": ollama_chat(question)["message"]["content"],
            "confidence": None,
            "sources": [],
        }

    if not retrieved_chunks:
        return {
            "answer": "I don't know based on the provided documents.",
            "confidence": None,
            "sources": [],
        }

    try:
        response = ollama_chat(
            build_prompt(
                question,
                retrieved_chunks,
                conversation_history,
                query_type,
            )
        )

    except Exception:
        return {
            "answer": "Sorry, something went wrong while generating the answer.",
            "confidence": None,
            "sources": [],
        }

    answer = response["message"]["content"].strip()

    if answer.startswith("I don't know"):
        return {
            "answer": answer,
            "confidence": None,
            "sources": [],
        }

    confidence = min(
        float(retrieved_chunks[0].get("confidence", 0)),
        1.0,
    )

    docs = {}

    for chunk in retrieved_chunks:
        docs.setdefault(chunk["source"], []).append(chunk["id"])

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": [
            {
                "document": doc,
                "chunks": sorted(set(ids)),
            }
            for doc, ids in docs.items()
        ],
    }


def stream_answer(
    question,
    retrieved_chunks,
    conversation_history=None,
    query_type=QueryType.DOCUMENT,
):

    if query_type == QueryType.CHAT:
        for chunk in ollama_chat(question, stream=True):
            if chunk["message"]["content"]:
                yield chunk["message"]["content"]
        return

    if not retrieved_chunks:
        yield "I don't know based on the provided documents."
        return

    try:

        for chunk in ollama_chat(
            build_prompt(
                question,
                retrieved_chunks,
                conversation_history,
                query_type,
            ),
            stream=True,
        ):

            if chunk["message"]["content"]:
                yield chunk["message"]["content"]

    except Exception:
        yield "Sorry, something went wrong while generating the answer."