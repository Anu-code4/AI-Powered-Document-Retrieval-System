"""
RAGAS Evaluator.
"""

import json

from datasets import Dataset
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

from config import MODEL_NAME


def evaluate_ragas(results):

    required = {
        "question",
        "generated_answer",
        "contexts",
        "expected_answer",
    }

    if any(required - row.keys() for row in results):
        raise ValueError("Invalid evaluation results.")

    dataset = Dataset.from_dict(
        {
            "question": [r["question"] for r in results],
            "answer": [r["generated_answer"] for r in results],
            "contexts": [r["contexts"] for r in results],
            "ground_truth": [
                r["expected_answer"] for r in results
            ],
        }
    )

    scores = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=ChatOllama(
            model=MODEL_NAME,
            temperature=0,
        ),
        embeddings=HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
        ),
    )

    df = scores.to_pandas()

    with open(
        "ragas_summary.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            df.mean(numeric_only=True).to_dict(),
            f,
            indent=4,
        )

    return df