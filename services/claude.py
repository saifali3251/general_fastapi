from services.llm_base import LLMBase
import anthropic
# from anthropic import Anthropic

class ClaudeLLM(LLMBase):
    def __init__(self, api_key: str):
        self.api_key = api_key
        # self.client = anthropic.Anthropic(api_key=api_key)

    def validate_api_key(self) -> dict:
        client = anthropic.Anthropic(api_key=self.api_key)            
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hello, respond with just 'OK'"}]
        )        
        if response and response.content:
            return {"valid": True, "message": "Claude API key is valid"}
        else:
            return {"valid": False, "message": "Invalid Claude API key"}



    def generate(self, prompt: str) -> str:
        message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=400,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
