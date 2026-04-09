"""
LLM Client for Azure OpenAI (Responses API compatible).
IMPORTANT: API key must be set as environment variable:
AZURE_LLM_API_KEY
"""

import os
import requests


class AzureLLMClient:

    def __init__(self):
        self.endpoint = "https://genia4as.services.ai.azure.com/api/projects/firstProject/openai/v1/responses"
        self.api_key = os.getenv("AZURE_LLM_API_KEY")

        if not self.api_key:
            raise ValueError("AZURE_LLM_API_KEY environment variable not set")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        payload = {
            "model": "gpt-4.1",
            "input": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"LLM Error: {response.text}")

        data = response.json()
        return data["output"][0]["content"][0]["text"]
