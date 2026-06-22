"""Agentic RAG pipeline with query rewrite and grader."""

from __future__ import annotations

import json
from pathlib import Path

DEMO = Path(__file__).resolve().parent.parent.parent / "demo-data"
_CHUNKS: list[dict] | None = None


def _load_chunks() -> list[dict]:
    global _CHUNKS
    if _CHUNKS is None:
        _CHUNKS = json.loads((DEMO / "owasp_chunks.json").read_text(encoding="utf-8"))
    return _CHUNKS


def rewrite_query(query: str) -> str:
    q = query.lower()
    if "injection" in q:
        return "OWASP A03 injection SQL XSS prevention"
    if "auth" in q:
        return "OWASP A07 identification authentication failures"
    return query


def retrieve(query: str, k: int = 3) -> list[dict]:
    rewritten = rewrite_query(query)
    terms = set(rewritten.lower().split())
    scored = []
    for c in _load_chunks():
        text = (c["title"] + " " + c["content"]).lower()
        score = sum(1 for t in terms if t in text)
        scored.append((score, c))
    scored.sort(key=lambda x: -x[0])
    return [c for _, c in scored[:k]]


def grade_chunks(query: str, chunks: list[dict]) -> tuple[bool, list[dict]]:
    if not chunks:
        return False, []
    relevant = [c for c in chunks if any(w in c["content"].lower() for w in query.lower().split()[:2])]
    return len(relevant) > 0, relevant or chunks[:1]


def agentic_rag_answer(query: str, context: dict) -> dict:
    trace = []
    rewritten = rewrite_query(query)
    trace.append({"step": "rewrite", "query": rewritten})
    chunks = retrieve(rewritten)
    trace.append({"step": "retrieve", "count": len(chunks)})
    ok, graded = grade_chunks(query, chunks)
    trace.append({"step": "grade", "passed": ok})
    if not ok:
        chunks = retrieve(query + " OWASP", k=5)
        trace.append({"step": "self_correct", "count": len(chunks)})
        _, graded = grade_chunks(query, chunks)
    answer = "\n".join(f"**{c['title']}**: {c['content'][:200]}" for c in graded)
    return {"answer": answer or "No relevant OWASP guidance found.", "trace": trace, "metadata": {"rewritten": rewritten}}
