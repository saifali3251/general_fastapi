import requests
import json
import re
from services.llm_base import LLMBase
import demjson3


class GroqLLM(LLMBase):
    def __init__(self, api_key: str, model: str = "llama3-70b-8192"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def validate_api_key(self):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            return {"valid": True, "message": "API key is valid"}
        except requests.exceptions.RequestException as e:
            return {"valid": False, "message": str(e)}


    def generate(self, prompt: str) -> list:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        print('Groq response is', response)
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        print('Groq content is', content)

        # Extract JSON array using regex
        match = re.search(r"\[\s*{.*?}\s*]", content, re.DOTALL)
        if not match:
            raise ValueError("Valid JSON array not found in the response.")

        raw_json = match.group(0)

        try:
            questions = demjson3.decode(raw_json)
            return questions
        except demjson3.JSONDecodeError as e:
            print("Error decoding JSON with demjson3:", str(e))
            raise ValueError("Failed to parse question JSON from LLM output.")



    # def generate(self, prompt: str) -> str:
    #     headers = {
    #         "Authorization": f"Bearer {self.api_key}",
    #         "Content-Type": "application/json"
    #     }
    #     payload = {
    #         "model": self.model,
    #         "messages": [{"role": "user", "content": prompt}],
    #         "temperature": 0.7,
    #         "max_tokens": 1000
    #     }
    #     response = requests.post(self.api_url, headers=headers, json=payload)
    #     print('Groq response is ',response)
    #     response.raise_for_status()
    #     content = response.json()["choices"][0]["message"]["content"]
    #     print('Groq content is ',content)
    #     # Clean and parse response
    #     raw_text = content.strip()
    #     json_str = re.sub(r"^```json|```$", "", raw_text).strip("`\n ")
    #     questions = json.loads(json_str)
    #     return questions
