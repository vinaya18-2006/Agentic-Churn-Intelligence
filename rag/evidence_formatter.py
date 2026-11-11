"""Format retrieved chunks into the shared evidence contract."""
from __future__ import annotations
from typing import Any

def format_evidence(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence = []
    for row in rows:
        text = str(row.get("text", "")).strip()
        metadata = dict(row.get("metadata") or {})
        source_id = str(metadata.get("source") or row.get("id") or "").strip()
        if not text or not source_id:
            continue
        evidence.append({"source_id": source_id, "text": text,
                         "metadata": {**metadata, "chunk_id": str(metadata.get("chunk_id") or row.get("id", ""))}})
    return evidence
