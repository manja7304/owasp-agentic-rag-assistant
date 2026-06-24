# Demo Walkthrough — OWASP Agentic RAG Assistant

**Pattern:** Agentic RAG  
**Captured:** 2026-06-24 with `USE_MOCK_LLM=true` (no Docker/Ollama required)

---

## Prerequisites

```bash
cp .env.example .env   # optional for mock demo
pip install -r requirements.txt
```

---

## Step 1 — One-command demo

```bash
export USE_MOCK_LLM=true
python scripts/run_demo.py
```

This runs the same FastAPI `TestClient` path as CI — real code, real JSON output.

### Step 2 — Agent API call

```bash
curl -X POST http://localhost:8080/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{"query": "How to prevent SQL injection in APIs?"}'
```

Or offline (no server):

```bash
USE_MOCK_LLM=true python scripts/run_demo.py
```

**Request (`demos/captured/request.json`):**

```json
{
  "query": "How to prevent SQL injection in APIs?"
}
```

**Response (`demos/captured/response.json`):**

```json
{
  "answer": "**A05 Security Misconfiguration**: Harden defaults and automate config review.",
  "trace": [
    {
      "step": "rewrite",
      "query": "OWASP A03 injection SQL XSS prevention"
    },
    {
      "step": "retrieve",
      "count": 3
    },
    {
      "step": "grade",
      "passed": false
    },
    {
      "step": "self_correct",
      "count": 5
    }
  ],
  "metadata": {
    "rewritten": "OWASP A03 injection SQL XSS prevention"
  }
}
```

### Step 3 — Agent trace excerpt

```json
[
  {
    "step": "rewrite",
    "query": "OWASP A03 injection SQL XSS prevention"
  },
  {
    "step": "retrieve",
    "count": 3
  }
]
```

---

## Architecture callout (2-min video)

> Agentic RAG: query rewrite → hybrid retrieval → self-grading → answer over OWASP/WSTG policy chunks with 25 gold eval Q&A.

Highlight in your recording:

1. **Problem → pattern** — why this agent architecture fits the security domain
2. **Tool/trace output** — show structured JSON, not just the final answer
3. **`docs/architecture.md`** — Mermaid diagram for the close

---

## Artifacts

| File | Description |
|------|-------------|
| [`demos/captured/request.json`](captured/request.json) | API request payload |
| [`demos/captured/response.json`](captured/response.json) | Live captured response |
| [`demos/captured/trace.json`](captured/trace.json) | Agent trace array |
| [`demos/captured/terminal-session.txt`](captured/terminal-session.txt) | Terminal replay for Loom |

---

## Record your video

```bash
python scripts/run_demo.py
```

Use [`demos/RECORDING_SCRIPT.md`](RECORDING_SCRIPT.md) for shot list and narration cues.
