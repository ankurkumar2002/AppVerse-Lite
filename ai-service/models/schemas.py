from pydantic import BaseModel
from typing import List


# ✅ Explain
class ExplainRequest(BaseModel):
    name: str
    description: str
    category: str


class ExplainResponse(BaseModel):
    summary: str
    use_cases: List[str]
    benefits: List[str]


# ✅ Chat
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# ✅ Assistant
class AssistantRequest(BaseModel):
    message: str


class AssistantResponse(BaseModel):
    reply: str