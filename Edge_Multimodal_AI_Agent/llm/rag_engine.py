"""
RAG Engine
----------------------------------------
Local Retrieval-Augmented Generation

Features
--------
✔ Load text documents
✔ Split into chunks
✔ Simple similarity search
✔ Build prompt for Ollama/LLaVA

Future Upgrade
--------------
Replace TF-IDF with:
- ChromaDB
- FAISS
- Sentence Transformers
"""

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGEngine:

    def __init__(self):

        self.documents = []

        self.file_names = []

        self.vectorizer = TfidfVectorizer()

        self.matrix = None

    # ----------------------------------

    def load_documents(self, folder="documents"):

        folder = Path(folder)

        if not folder.exists():
            return

        self.documents.clear()
        self.file_names.clear()

        for file in folder.glob("*.txt"):

            try:

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                self.documents.append(text)

                self.file_names.append(file.name)

            except Exception:
                pass

        if self.documents:

            self.matrix = self.vectorizer.fit_transform(
                self.documents
            )

    # ----------------------------------

    def search(self,
               query,
               top_k=3):

        if self.matrix is None:
            return []

        q = self.vectorizer.transform([query])

        scores = cosine_similarity(
            q,
            self.matrix
        )[0]

        order = scores.argsort()[::-1]

        results = []

        for index in order[:top_k]:

            results.append({

                "file": self.file_names[index],

                "score": float(scores[index]),

                "text": self.documents[index][:1000]

            })

        return results

    # ----------------------------------

    def build_context(self,
                      query):

        docs = self.search(query)

        context = ""

        for d in docs:

            context += (
                f"\nDocument : {d['file']}\n"
                f"{d['text']}\n"
            )

        return context

    # ----------------------------------

    def build_prompt(self,
                     question):

        context = self.build_context(question)

        prompt = f"""

You are a Smart Workspace Security AI.

Answer using ONLY the retrieved context.

Context

{context}

Question

{question}

Answer:

"""

        return prompt