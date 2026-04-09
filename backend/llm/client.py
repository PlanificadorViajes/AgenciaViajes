import os
import requests


class AzureLLMClient:
    """
    Centralized Azure OpenAI client for the backend.
    Reads API key from environment variable:
    AZURE_LLM_API_KEY
    """

    def __init__(self):
        self.endpoint = os.getenv(
            "AZURE_LLM_ENDPOINT",
            "https://genia4as.services.ai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2024-02-15-preview",
        )
        self.api_key = os.getenv("AZURE_LLM_API_KEY")

        if not self.api_key:
            raise ValueError(
                "AZURE_LLM_API_KEY environment variable not set in backend environment"
            )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"LLM Error: {response.text}")

        data = response.json()

        # Azure Chat Completions format
        return data["choices"][0]["message"]["content"]
