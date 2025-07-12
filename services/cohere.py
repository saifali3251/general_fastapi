from services.llm_base import LLMBase
import cohere
import re, json
import demjson3

class CohereLLM(LLMBase):
    def __init__(self, api_key: str):
        self.client = cohere.Client(api_key)
        self.api_key = api_key
    
    def validate_api_key(self) -> dict:
        # co = cohere.ClientV2(self.api_key)
        # response = co.chat(
        #     model="command-a-03-2025", 
        #     messages=[{"role": "user", "content": "hello world!"}]
        # )

        co = cohere.Client(self.api_key)
        # Make a simple test call
        response = co.generate(
            model='command',
            prompt="Hello, respond with just 'OK'",
            max_tokens=10
        )        
        if response and response.generations:
            return {"valid": True, "message": "Cohere API key is valid"}
        else:
            return {"valid": False, "message": "Invalid Cohere API key"}

    def generate(self, prompt: str):
        response = self.client.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=800,
            temperature=0.7
        )

        raw_text = response.generations[0].text.strip()
        print('Raw text is ->', raw_text)

        # Step 1: Clean up markdown formatting or backticks
        cleaned = re.sub(r"^```json|```$", "", raw_text).strip("`\n ")

        # Step 2: Try to fix and decode using demjson3
        try:
            questions = demjson3.decode(cleaned)
            if isinstance(questions, list):
                return questions
            else:
                print("⚠️ Parsed JSON is not a list.")
        except demjson3.JSONDecodeError as e:
            print("🚨 demjson3 failed to parse the response:", str(e))

        # Fallback: return a dummy informative question to avoid empty UI
        return [{
            "question": "⚠️ Unable to generate questions. Please try again.",
            "options": ["Retry", "Wait", "Switch model", "Check network"],
            "correctAnswer": "Retry",
            "explanation": "The model's response couldn't be parsed. This might be due to truncation or malformed JSON.",
            "difficulty": "N/A",
            "season": "N/A",
            "character": "N/A",
            "category": "System"
        }]