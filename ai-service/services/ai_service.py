import google.generativeai as genai
from core.Config import settings
import time

category_cache = {}

from utils.prompt_templates import(
    explain_prompt,
    chat_prompt,
    assistant_prompt
)

import json

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


# def generate_chat(message, session_id): 
#     prompt = chat_prompt(message)
#     return call_llm(prompt)

# def generate_assistant_reply(message):
#     prompt = assistant_prompt(message)
#     return call_llm(prompt)

genai.configure(api_key=settings.GEMINI_API_KEY)

model= genai.GenerativeModel("models/gemini-2.5-flash")



def call_llm(prompt: str):
    retries = 3

    for attempt in range(retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 200,
                    "temperature": 0.7
                }
            )
            return response.text

        except Exception as e:
            print("LLM ERROR:", e)   # ✅ ADD THIS

            if "429" in str(e) or "503" in str(e):
                time.sleep(1.5 * (attempt + 1))
                continue
            raise e

    return "Sorry, please try again."


def detect_category_ai(query: str, categories: list):
    if query in category_cache:
        return category_cache[query]

    prompt = f"""
Classify the user query into ONE of these categories:

{", ".join(categories)}

Query: {query}

Return only the category name.
"""

    response = call_llm(prompt)
    result = response.strip()

    # clean
    result = result.replace(".", "").strip()

    # validate
    for c in categories:
        if c.lower() == result.lower():
            category_cache[query] = c
            return c

    return None


def build_documents(apps):
    docs = [
        f"{app['name']} {app['category']} {app['description']}"
        for app in apps
    ]
    return docs

def generate_overview(query, results):

    context = "\n".join(results)

    prompt = f"""
        User query: {query}

        Relevant apps:
        {context}

        Explain briefly why these apps are useful.
        """

    # response = model.generate_content(prompt)

    return call_llm(prompt)