"""
Query Rewriter.
"""

import re

from ollama import chat

from config import MODEL_NAME


FOLLOW_UP_WORDS = {
    "it", "its", "this", "that",
    "they", "them", "their",
}


def rewrite_query(question, conversation_history=None):

    if (
        not conversation_history
        or not any(
            w in FOLLOW_UP_WORDS
            for w in re.findall(r"\w+", question.lower())
        )
    ):
        return question

    previous = next(
        (
            m["content"]
            for m in reversed(conversation_history)
            if m["role"] == "user"
        ),
        "",
    )

    prompt = f"""
Rewrite the follow-up question into a standalone question.

Rules:
- Use ONLY the previous user question.
- Replace pronouns with its main subject.
- Return ONLY the rewritten question.

Previous:
{previous}

Current:
{question}
"""

    try:
        rewritten = (
            chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0},
            )["message"]["content"].strip()
            or question
        )

        print(f"{question} -> {rewritten}")
        return rewritten

    except Exception:
        return question