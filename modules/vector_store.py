import os
import uuid
from typing import List, Dict, Any

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np

import os

EMBED_MODEL_PATH = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

class RAGStore:
    def __init__(self, persist_dir: str = None, collection_name: str = "guidelines"):
        self.persist_dir = persist_dir or os.getenv("CHROMA_DIR", "data/embeddings")
        self.client = chromadb.PersistentClient(path=self.persist_dir, settings=Settings(allow_reset=False))
        self.collection = self.client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
        self.embedder = SentenceTransformer(EMBED_MODEL_PATH)

    def _embed(self, texts: List[str]) -> List[List[float]]:
        return self.embedder.encode(texts, normalize_embeddings=True).tolist()

    def add_documents(self, chunks: List[str], metadoc: Dict[str, Any] = None):
        ids = [str(uuid.uuid4()) for _ in chunks]
        embeddings = self._embed(chunks)
        metadata = []
        for i, ch in enumerate(chunks):
            md = {"chunk_id": i}
            if metadoc:
                md.update(metadoc)
            metadata.append(md)

        self.collection.add(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadata)

    def search(self, query: str, top_k: int = 5):
        q_emb = self._embed([query])[0]
        res = self.collection.query(query_embeddings=[q_emb], n_results=top_k, include=["documents", "metadatas", "distances"])
        results = []
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]
        for d, m, dist in zip(docs, metas, dists):
            results.append({"text": d, "source": m.get("source","unknown"), "score": 1 - dist})
        return results
