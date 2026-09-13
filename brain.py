import base64
import os
import re
import requests
from systemprompt import systemprompt
from getxt import getxt
api_key = None
api_key=getxt("apikey.txt")

MODEL = "google/gemini-2.5-flash-lite"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

systemprompt = systemprompt
def is_plan(text):
    return str(text).strip().lower().startswith("plan:")


def trim_session(session):
    updated_session = []
    action_count = 0
    for message in reversed(session):
        if is_plan(message["content"]):
            updated_session.append(message)
        else:
            if action_count < 2:
                updated_session.append(message)
                action_count += 1
    new_session = list(reversed(updated_session))
    return new_session
def brain(image_bytes, session, prompt, api_key=api_key):
    # Initialize a new session if none is provided
    if session is None:
        session = [{"role": "system", "content": systemprompt}]
    
    img = base64.b64encode(image_bytes).decode()
    
    # Append current turn
    session.append({
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}}
        ]
    })
    
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-site.com", 
            },
            json={"model": MODEL, "messages": session},
            timeout=15 
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        # Remove the user message we just added so it doesn't break future calls
        session.pop() 
        return None, session

    out = data["choices"][0]["message"]["content"]

    session.append({"role": "assistant", "content": out})

    session=trim_session(session)

    return out, session
