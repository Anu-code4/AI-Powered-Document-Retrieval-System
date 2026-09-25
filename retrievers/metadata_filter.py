"""
Metadata Filter.
"""

import re


def extract_metadata_filter(query: str) -> dict:

    query = query.lower()
    filters = {}

    if "pdf" in query:
        filters["file_type"] = ".pdf"
    elif "docx" in query:
        filters["file_type"] = ".docx"

    match = re.search(
        r"([\w\-]+\.(?:pdf|docx))",
        query,
    )

    if match:
        filters["source"] = match.group(1)

    return filters