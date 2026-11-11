"""Persistent ChromaDB vector store."""
from __future__ import annotations
from pathlib import Path
from typing import Any

class ChromaVectorStore:
    def __init__(self, persist_directory: str = "data/chroma", collection_name: str = "churn_knowledge"):
        try:
            import chromadb
        except ImportError as exc:
            raise RuntimeError("Install chromadb to use the vector store.") from exc
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

    def add(self, chunks: list[dict[str, Any]], embeddings: list[list[float]]) -> int:
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have exactly one embedding.")
        if not chunks:
            return 0
        self.collection.upsert(
            ids=[c["id"] for c in chunks],
            documents=[c["text"] for c in chunks],
            embeddings=embeddings,
            metadatas=[{k: (v if isinstance(v, (str, int, float, bool)) else str(v))
                        for k, v in c["metadata"].items()} for c in chunks],
        )
        return len(chunks)

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict[str, Any]]:
        if top_k < 1:
            return []
        result = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        rows = []
        ids = (result.get("ids") or [[]])[0]
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]
        for i, doc_id in enumerate(ids):
            distance = distances[i] if i < len(distances) else None
            rows.append({"id": doc_id, "text": docs[i], "metadata": metas[i] or {},
                         "score": (1.0 - float(distance)) if distance is not None else 0.0})
        return rows
