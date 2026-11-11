"""Load PDF, TXT and CSV knowledge-base documents with source metadata."""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Any

SUPPORTED = {".pdf", ".txt", ".csv"}

def load_documents(paths: list[str | Path]) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"Knowledge-base file not found: {path}")
        suffix = path.suffix.lower()
        if suffix not in SUPPORTED:
            raise ValueError(f"Unsupported file type {suffix}: {path}")
        if suffix == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            for page_no, page in enumerate(reader.pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    documents.append({"text": text, "source": str(path), "page": page_no})
        elif suffix == ".txt":
            text = path.read_text(encoding="utf-8", errors="replace").strip()
            if text:
                documents.append({"text": text, "source": str(path)})
        else:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                for row_no, row in enumerate(csv.DictReader(handle), start=2):
                    text = " | ".join(f"{k}: {v}" for k, v in row.items() if v not in (None, ""))
                    if text.strip():
                        documents.append({"text": text, "source": str(path), "row": row_no})
    return documents
