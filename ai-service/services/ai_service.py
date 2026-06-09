import google.generativeai as genai
from core.Config import settings

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


def generate_chat(message) :
    prompt = chat_prompt(message)
    return call_llm(prompt)

def generate_assistant_reply(message):
    prompt = assistant_prompt(message)
    return call_llm(prompt)

genai.configure(api_key=settings.GEMINI_API_KEY)

model= genai.GenerativeModel("models/gemini-2.5-flash")


def call_llm(prompt: str):
    response = model.generate_content(prompt)
    return response.text