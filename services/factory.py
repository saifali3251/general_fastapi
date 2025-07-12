from services.gemini import GeminiLLM
from services.claude import ClaudeLLM
from services.mistral import MistralLLM
from services.cohere import CohereLLM
from services.llm_base import LLMBase
from services.groq import GroqLLM

def get_llm_provider(model_name: str, api_key: str | None) -> LLMBase:
    model_name = model_name.lower()
    if model_name == "gemini":
        return GeminiLLM(api_key)
    elif model_name == "groq":
        return GroqLLM(api_key)
    elif model_name == "claude":
        return ClaudeLLM(api_key)
    elif model_name == "cohere":
        return CohereLLM(api_key)
    elif model_name == "mistral":
        return MistralLLM()
    raise ValueError(f"Unsupported model: {model_name}")
