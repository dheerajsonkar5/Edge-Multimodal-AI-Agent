from pathlib import Path

class DocumentLoader:

    def __init__(self,
                 folder="documents"):

        self.folder = Path(folder)

        self.folder.mkdir(exist_ok=True)

    def load_documents(self):

        docs = []

        for file in self.folder.glob("*.txt"):

            docs.append(file.read_text(
                encoding="utf-8",
                errors="ignore"
            ))

        return docs

    def split_documents(self,
                        docs,
                        chunk_size=500):

        chunks = []

        for doc in docs:

            for i in range(0, len(doc), chunk_size):

                chunks.append(doc[i:i+chunk_size])

        return chunks