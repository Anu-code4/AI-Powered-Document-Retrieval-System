"""
Generate multiple search queries.
"""

from ollama import chat

from config import MODEL_NAME


def generate_multi_queries(question: str) -> list[str]:

    prompt = f"""
Generate 4 different search queries.

Rules:
- Preserve meaning.
- Use different wording.
- One query per line.
- No numbering.
- No explanation.

Question:
{question}
""".strip()

    try:
        response = chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2},
        )

        queries = [
            line.strip()
            for line in response["message"]["content"].splitlines()
            if line.strip()
        ]

        return list(dict.fromkeys([*queries, question]))

    except Exception:
        return [question]