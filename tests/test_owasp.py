from src.rag.pipeline import agentic_rag_answer, rewrite_query

def test_rewrite():
    assert "injection" in rewrite_query("SQL injection risks").lower()

def test_rag():
    out = agentic_rag_answer("How to prevent injection?", {})
    assert out["answer"]
    assert len(out["trace"]) >= 2
