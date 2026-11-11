"""Deterministic character-based chunking with overlap."""
from __future__ import annotations
import hashlib
import re
from typing import Any

def split_documents(documents: list[dict[str, Any]], chunk_size: int = 900,
                    chunk_overlap: int = 150) -> list[dict[str, Any]]:
    if chunk_size < 1 or chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("Require chunk_size > chunk_overlap >= 0.")
    chunks = []
    for doc_index, doc in enumerate(documents):
        text = re.sub(r"\s+", " ", str(doc.get("text", ""))).strip()
        if not text:
            continue
        source = str(doc.get("source", f"document-{doc_index}"))
        step = chunk_size - chunk_overlap
        for start in range(0, len(text), step):
            part = text[start:start + chunk_size].strip()
            if not part:
                continue
            chunk_id = hashlib.sha256(f"{source}:{start}:{part}".encode()).hexdigest()[:20]
            metadata = {k: v for k, v in doc.items() if k != "text"}
            metadata.update({"source": source, "chunk_id": chunk_id, "start": start})
            chunks.append({"id": chunk_id, "text": part, "metadata": metadata})
            if start + chunk_size >= len(text):
                break
    return chunks
