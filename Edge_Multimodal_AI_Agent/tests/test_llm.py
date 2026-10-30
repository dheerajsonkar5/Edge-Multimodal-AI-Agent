# tests/test_llm.py
import unittest
from llm.prompt_engine import PromptEngine

class TestLLMPrompts(unittest.TestCase):
    def test_prompt_construction(self):
        """
        Validates that telemetry translation layers generate strings correctly without missing parameters.
        """
        mock_telemetry = {
            "person_present": True,
            "posture_metrics": {"status": "normal", "slouching_detected": False},
            "workspace_anomalies": []
        }
        
        prompt = PromptEngine.build_reasoning_prompt(mock_telemetry)
        
        # Matrix parameter checks inside prompt string boundaries
        self.assertIsInstance(prompt, str)
        self.assertIn("WORKSPACE REALTIME TELEMETRY MATRIX", prompt)
        self.assertIn("User Presence Detected: True", prompt)

if __name__ == "__main__":
    unittest.main()