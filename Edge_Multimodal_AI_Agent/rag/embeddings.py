import ollama

class EmbeddingModel:

    def __init__(self,
                 model="nomic-embed-text"):

        self.model = model

    def encode(self, text):

        try:

            response = ollama.embeddings(
                model=self.model,
                prompt=text
            )

            return response["embedding"]

        except Exception:

            return [0.0] * 768