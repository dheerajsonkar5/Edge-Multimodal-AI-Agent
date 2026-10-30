from pathlib import Path
import json

class VectorStore:
    """
    Lightweight local vector store.
    (Can later be replaced with ChromaDB / FAISS)
    """

    def __init__(self):

        self.db = []

    def add(self, embedding, text):

        self.db.append({
            "embedding": embedding,
            "text": text
        })

    def save(self, file="rag/vector_db.json"):

        Path(file).parent.mkdir(exist_ok=True)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.db, f)

    def load(self, file="rag/vector_db.json"):

        if Path(file).exists():

            with open(file, "r", encoding="utf-8") as f:

                self.db = json.load(f)

    def search(self, query_embedding, top_k=3):

        if len(self.db) == 0:
            return []

        scores = []

        for item in self.db:

            score = sum(
                a*b for a, b in zip(query_embedding,
                                    item["embedding"])
            )

            scores.append((score, item["text"]))

        scores.sort(reverse=True)

        return [x[1] for x in scores[:top_k]]