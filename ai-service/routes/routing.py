from fastapi import APIRouter


from services.ai_service import (
    detect_category_ai,
    build_documents,
    generate_overview
)

from springRequests.fetchAppsByCategory import fetch_apps_by_category
from rag.RagService import search_apps


from models.schemas import (
    ExplainRequest,
    ExplainResponse,
    ChatRequest,
    ChatResponse,
    AssistantRequest,
    AssistantResponse
)

from services.ai_service import (
    generate_explanation
    
)

from utils.AiFunctions import (generate_chat,generate_assistant_reply)

router = APIRouter(prefix="/ai")


# ✅ Explain (structured)
@router.post("/explain", response_model=ExplainResponse)
def explain_app(request: ExplainRequest):
    return generate_explanation(request)


# ✅ Chat
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = generate_chat(request.message, request.session_id)
    return {"reply": reply}


# ✅ Assistant
@router.post("/assistant", response_model=AssistantResponse)
def assistant(request: AssistantRequest):
    reply = generate_assistant_reply(request.message)
    return {"reply": reply}


@router.post("/search")
def ai_search(request: dict):

    query = request["query"]

    # ✅ Step 1: categories (can be fixed or fetched later)
    categories = ["Finance", "Entertainment", "Health", "Productivity"]

    category = detect_category_ai(query, categories)

    if not category:
        return {"message": "No matching category"}

    # ✅ Step 2: fetch apps
    apps = fetch_apps_by_category(category)
    
    print("APPS RAW:", apps)
    print("TYPE:", type(apps))


    if not apps:
        return {"message": "No apps found"}

    # ✅ Step 3: build docs
    docs = build_documents(apps)

    # ✅ Step 4: search
    results = search_apps(query, docs)

    # ✅ Step 5: summary
    overview = generate_overview(query, results)

    return {
        "category": category,
        "apps": results,
        "overview": overview
    }
