from fastapi import APIRouter

from models.schemas import (
    ExplainRequest,
    ExplainResponse,
    ChatRequest,
    ChatResponse,
    AssistantRequest,
    AssistantResponse
)

from services.ai_service import (
    generate_explanation,
    generate_chat,
    generate_assistant_reply
)

router = APIRouter(prefix="/ai")


# ✅ Explain (structured)
@router.post("/explain", response_model=ExplainResponse)
def explain_app(request: ExplainRequest):
    return generate_explanation(request)


# ✅ Chat
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = generate_chat(request.message)
    return {"reply": reply}


# ✅ Assistant
@router.post("/assistant", response_model=AssistantResponse)
def assistant(request: AssistantRequest):
    reply = generate_assistant_reply(request.message)
    return {"reply": reply}
