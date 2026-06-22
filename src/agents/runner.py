"""Agentic RAG: rewrite → retrieve → grade → answer."""

from __future__ import annotations

import json

from src.rag.pipeline import agentic_rag_answer


def run_agent(query: str, context: dict | None = None) -> dict:
    return agentic_rag_answer(query, context or {})
