import json
# from chat_memory import chat_memory, MAX_HISTORY


from collections import defaultdict
from services.ai_service import call_llm

chat_memory = defaultdict(list)
MAX_HISTORY = 6


PORTAL_DOCS = [
    "To upload an app, go to the dashboard and click the Upload button.",
    "To edit an app, open the dashboard and select the app you want to edit.",
    "Users can search for applications using the search bar or by choosing a category.",
    "Click on an app card to view the application details.",
    "Applications may contain details such as name, category, and description.",
    "Users can browse apps in categories like Finance, Entertainment, Health, and Productivity."
]

def generate_explanation(data):
    prompt = explain_prompt(data.name, data.description, data.category)

    raw = call_llm(prompt)

    try:
        return json.loads(raw)
    except:
        return {
            "summary" : raw,
            "use_cases" : [],
            "benefits" : []
        }



def generate_chat(message, session_id):
    # ✅ get last few messages
    history = "\n".join(chat_memory[session_id][-MAX_HISTORY:])

    prompt = f"""
You are a helpful AI assistant.

Conversation:
{history}

User: {message}
Assistant:
"""

    reply = call_llm(prompt)

    # ✅ store history
    chat_memory[session_id].append(f"User: {message}")
    chat_memory[session_id].append(f"Assistant: {reply}")

    return reply



def generate_assistant_reply(message):
    # ✅ retrieve relevant portal documents
    results = search_apps(message, PORTAL_DOCS)

    context = "\n".join(results)

    prompt = f"""
You are a helpful assistant for the application portal.

Use the context below to answer the user's question.
If the answer is not clearly available in the context, say:
"I could not find that in the portal knowledge."

Context:
{context}

User question:
{message}

Answer briefly and clearly.
"""

    return call_llm(prompt)
