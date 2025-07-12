from abc import ABC, abstractmethod

class LLMBase(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
    
    @abstractmethod
    def validate_api_key(self) -> dict:
        pass