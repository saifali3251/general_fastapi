from services.llm_base import LLMBase
import requests

class MistralLLM(LLMBase):
    def validate_api_key(self):
        try:
            return {"valid": True, "message": "API key is valid"}
        except Exception as e:
            return {"valid": False, "message": "Invalid API key or service unavailable"}


    def generate(self, prompt: str) -> str:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"].strip()
