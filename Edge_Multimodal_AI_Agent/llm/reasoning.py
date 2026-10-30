from llm.prompt_engine import PromptEngine
from llm.ollama_client import OllamaClient


class WorkspaceReasoning:

    def __init__(self):

        self.client = OllamaClient()

    def analyse(self, vision_result):

        prompt = PromptEngine.build_prompt(

            vision_result

        )

        response = self.client.generate(

            prompt

        )

        return response