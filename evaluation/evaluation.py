"""
Evaluation Pipeline.
"""

import csv
import json

from llm.generator import generate_answer
from retrievers.hybrid_retriever import hybrid_retriever

from .evaluation_dataset import evaluation_data
from .ragas_evaluator import evaluate_ragas


def evaluate():

    results = []

    for item in evaluation_data:

        try:

            docs = hybrid_retriever(
                item["question"],
                top_k=5,
            )

            results.append(
                {
                    "question": item["question"],
                    "expected_answer": item["expected_answer"],
                    "generated_answer": generate_answer(
                        item["question"],
                        docs,
                    )["answer"],
                    "contexts": [
                        doc["text"] for doc in docs
                    ],
                }
            )

        except Exception as e:

            results.append(
                {
                    "question": item["question"],
                    "expected_answer": item["expected_answer"],
                    "generated_answer": f"ERROR: {e}",
                    "contexts": [],
                }
            )

    return results


def save_results(results):

    fields = (
        "question",
        "expected_answer",
        "generated_answer",
        "contexts",
    )

    with open(
        "evaluation_results.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            {
                **row,
                "contexts": "\n\n".join(
                    row["contexts"]
                ),
            }
            for row in results
        )

    with open(
        "evaluation_results.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False,
        )


if __name__ == "__main__":

    results = evaluate()

    save_results(results)

    evaluate_ragas(results).to_csv(
        "ragas_results.csv",
        index=False,
    )

    print("✅ Evaluation completed.")