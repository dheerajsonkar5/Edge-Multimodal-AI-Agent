from datetime import datetime


class PromptEngine:

    @staticmethod
    def build_prompt(status):

        prompt = f"""
You are an Edge Multimodal AI Security Agent.

Current Time:
{datetime.now()}

Workspace Status

Faces Detected:
{status['faces']}

Persons Detected:
{status['persons']}

Eyes Detected:
{status['eyes']}

Objects:
{status['objects']}

Instructions

1. Analyse workspace safety.

2. Detect suspicious activity.

3. Check user attentiveness.

4. Generate alert if required.

5. Give short recommendations.

Return professional report.
"""

        return prompt