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