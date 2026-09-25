"""
Query Router.
"""

from enum import Enum


class QueryType(Enum):
    DOCUMENT = "document"
    MEMORY = "memory"
    CHAT = "chat"


MEMORY_KEYWORDS = (
    "previous",
    "earlier",
    "before",
    "last question",
    "history",
    "conversation",
    "remember",
)

CHAT_KEYWORDS = (
    "hi",
    "hello",
    "hey",
    "bye",
    "goodbye",
    "thanks",
    "thank you",
    "good morning",
    "good afternoon",
    "good evening",
    "good night",
)


def route_query(query: str) -> QueryType:

    query = query.lower().strip()

    if any(word in query for word in MEMORY_KEYWORDS):
        return QueryType.MEMORY

    if any(word in query for word in CHAT_KEYWORDS):
        return QueryType.CHAT

    return QueryType.DOCUMENT