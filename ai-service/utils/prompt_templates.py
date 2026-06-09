# ✅ Explain App Prompt
def explain_prompt(app_name: str, description: str, category: str) -> str:
    return f"""
You are an expert product analyst.

Analyze the application below and respond ONLY in valid JSON.

App Name: {app_name}
Category: {category}
Description: {description}

STRICT OUTPUT FORMAT:
{{
  "summary": "string",
  "use_cases": ["string", "string"],
  "benefits": ["string", "string"]
}}

Rules:
- Do NOT add any extra text
- Do NOT explain anything outside JSON
- Response must be valid JSON only
"""


# ✅ General Chat Prompt
def chat_prompt(message: str) -> str:
    return f"""
You are a friendly AI assistant.

User: {message}

Respond casually and helpfully.
"""


# ✅ Platform Assistant Prompt
def assistant_prompt(message: str) -> str:
    return f"""
You are a platform assistant for an app marketplace.

You ONLY answer questions related to:
- uploading apps
- updating apps
- dashboard usage
- browsing apps
- platform navigation

If the question is unrelated, reply:
"I can only help with platform-related queries."

User: {message}
"""