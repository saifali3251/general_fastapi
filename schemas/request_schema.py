from pydantic import BaseModel
from typing import Optional

# class PromptRequest(BaseModel):
#     prompt: str
#     model_name: str
#     api_key: str | None = None
# schemas/request_schema.py

class PromptRequest(BaseModel):
    prompt: str
    model_name: str
    api_key: Optional[str] = None
    name: str
    type: str
    is_test : bool

class PromptRequest1(BaseModel):
    prompt: str
    model_name: str
    name: str
    type: str




class ApiKeyRequest(BaseModel):
    api_key: Optional[str] = None
    model_name : str
