"""
Main application entry point.
"""

import logging

from config import TOP_K
from llm.generator import generate_answer, stream_answer
from llm.query_rewriter import rewrite_query
from memory.memory import ConversationMemory
from query_router import QueryType, route_query
from retrievers.hybrid_retriever import hybrid_retriever
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

memory = ConversationMemory(max_history=5)


def retrieve(query: str):

    history = memory.get_history()
    query_type = route_query(query)

    print(f"Query Type: {query_type}")

    if query_type != QueryType.DOCUMENT:
        return query_type, query, [], history

    query = rewrite_query(
        question=query,
        conversation_history=history,
    )

    chunks = hybrid_retriever(
        query=query,
        top_k=TOP_K,
    )

    return query_type, query, chunks, history


def get_answer(query: str) -> dict:

    query_type, question, chunks, history = retrieve(query)

    result = generate_answer(
        question=question,
        retrieved_chunks=chunks,
        conversation_history=history,
        query_type=query_type,
    )

    memory.add_user_message(query)
    memory.add_ai_message(result["answer"])

    return result


def stream_response(query: str):

    query_type, question, chunks, history = retrieve(query)

    answer = ""

    for token in stream_answer(
        question=question,
        retrieved_chunks=chunks,
        conversation_history=history,
        query_type=query_type,
    ):
        answer += token
        yield token

    memory.add_user_message(query)
    memory.add_ai_message(answer)


def main():

    print("\n🚀 AI-Powered Document Retrieval System Ready\n")

    while True:

        query = input("Ask: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            continue

        result = get_answer(query)

        print(f"\nAnswer:\n{result['answer']}")
        print("-" * 80)


if __name__ == "__main__":
    main()