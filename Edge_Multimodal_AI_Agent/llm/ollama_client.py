import requests

from core.config import settings
from core.logger import logger


class OllamaClient:

    def __init__(self):

        self.url = settings.OLLAMA_URL.rstrip("/")

        self.model = settings.OLLAMA_MODEL

    def generate(self, prompt):

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False

        }

        try:

            response = requests.post(

                f"{self.url}/api/generate",

                json=payload,

                timeout=120

            )

            response.raise_for_status()

            return response.json()["response"]

        except Exception as e:

            logger.error(e)

            return f"Ollama Error : {e}"