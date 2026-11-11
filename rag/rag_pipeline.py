"""Ingestion and retrieval orchestration."""
from __future__ import annotations
from pathlib import Path
from .document_loader import load_documents
from .text_splitter import split_documents
from .embeddings import SentenceEmbeddingModel
from .vector_store import ChromaVectorStore
from .keyword_retriever import BM25KeywordRetriever
from .hybrid_retriever import HybridRetriever
from .evidence_formatter import format_evidence

class RAGPipeline:
    def __init__(self, persist_directory="data/chroma",
                 model_name="sentence-transformers/all-MiniLM-L6-v2",
                 chunk_size=900, chunk_overlap=150):
        self.embedding_model = SentenceEmbeddingModel(model_name)
        self.vector_store = ChromaVectorStore(persist_directory)
        self.keyword_retriever = BM25KeywordRetriever()
        self.chunk_size, self.chunk_overlap = chunk_size, chunk_overlap
        self._chunks = []
        self.hybrid = HybridRetriever(self.vector_store, self.embedding_model, self.keyword_retriever)

    def ingest_files(self, paths: list[str | Path]) -> int:
        docs = load_documents(paths)
        chunks = split_documents(docs, self.chunk_size, self.chunk_overlap)
        vectors = self.embedding_model.encode([c["text"] for c in chunks])
        count = self.vector_store.add(chunks, vectors)
        self._chunks = chunks
        self.keyword_retriever.fit(chunks)
        return count

    def ingest_documents(self, documents: list[dict]) -> int:
        chunks = split_documents(documents, self.chunk_size, self.chunk_overlap)
        vectors = self.embedding_model.encode([c["text"] for c in chunks])
        count = self.vector_store.add(chunks, vectors)
        self._chunks = chunks
        self.keyword_retriever.fit(chunks)
        return count

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        if not query.strip():
            return []
        return format_evidence(self.hybrid.search(query, top_k))
