#!/usr/bin/env python3
import json
from pathlib import Path

OWASP = [
    ("A01 Broken Access Control", "Enforce least privilege and deny by default."),
    ("A02 Cryptographic Failures", "Use strong algorithms and protect keys at rest and in transit."),
    ("A03 Injection", "Use parameterized queries and input validation."),
    ("A04 Insecure Design", "Threat model and secure design patterns in SDLC."),
    ("A05 Security Misconfiguration", "Harden defaults and automate config review."),
    ("A06 Vulnerable Components", "Maintain SBOM and patch dependencies."),
    ("A07 Auth Failures", "MFA, secure session management, credential stuffing defenses."),
    ("A08 Data Integrity", "Verify software supply chain and CI/CD integrity."),
    ("A09 Logging Failures", "Centralize logs and protect audit trails."),
    ("A10 SSRF", "Validate and sandbox outbound requests."),
]
DEMO = Path(__file__).resolve().parent.parent / "demo-data"
DEMO.mkdir(parents=True, exist_ok=True)
chunks = [{"id": f"owasp-{i}", "title": t, "content": c} for i, (t, c) in enumerate(OWASP, 1)]
(DEMO / "owasp_chunks.json").write_text(json.dumps(chunks, indent=2), encoding="utf-8")
# Gold eval set
# Expand to 25 eval questions (repeat with variants if needed)
eval_q = []
for i in range(25):
    t, c = OWASP[i % len(OWASP)]
    eval_q.append({"question": f"What is OWASP {t} (Q{i+1})?", "ground_truth": c})
(DEMO / "eval_questions.json").write_text(json.dumps(eval_q, indent=2), encoding="utf-8")
print(f"Seeded {len(chunks)} OWASP chunks and {len(eval_q)} eval questions")
