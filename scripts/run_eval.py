#!/usr/bin/env python3
"""RAGAS-style eval on demo gold set (simplified metrics without live LLM)."""

import json
from pathlib import Path

from src.rag.pipeline import agentic_rag_answer

DEMO = Path(__file__).resolve().parent.parent / "demo-data"


def faithfulness(answer: str, context: str) -> float:
    words = set(context.lower().split())
    hit = sum(1 for w in answer.lower().split() if w in words)
    return min(1.0, hit / max(len(answer.split()), 1))


def main():
    questions = json.loads((DEMO / "eval_questions.json").read_text(encoding="utf-8"))
    scores = []
    for item in questions:
        result = agentic_rag_answer(item["question"], {})
        ctx = item["ground_truth"]
        scores.append(faithfulness(result["answer"], ctx))
    avg = sum(scores) / len(scores) if scores else 0
    print(json.dumps({"faithfulness_avg": round(avg, 3), "n": len(scores)}))


if __name__ == "__main__":
    main()
