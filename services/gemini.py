import google.generativeai as genai
from services.llm_base import LLMBase
import json,re
from dotenv import load_dotenv

class GeminiLLM(LLMBase):
    def __init__(self, api_key: str):
        load_dotenv()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")
        self.api_key = api_key
    
    def validate_api_key(self):
        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content("Hello")
            return {"valid": True, "message": "API key is valid"}
        
        except Exception as e:
            return {"valid": False, "message": "Invalid API key or service unavailable"}


    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        # Clean response
        raw_text = response.text.strip()
        json_str = re.sub(r"^```json|```$", "", raw_text).strip("` \n")
        questions = json.loads(json_str)
        return questions
