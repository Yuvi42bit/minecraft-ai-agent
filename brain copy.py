import base64
import os
import re
import requests
from systemprompt import systemprompt
api_key = None
with open("apikey.txt", "r") as file:
    api_key = file.read().strip()
MODEL = "google/gemini-2.5-flash-lite"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

systemprompt = systemprompt

ACTION_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*\(.*?\)\s*$")

def is_plan(text):
    return str(text).strip().lower().startswith("plan:")

def is_action(text):
    text = str(text).strip()
    return text == "break" or bool(ACTION_RE.match(text))

def normalize_output(out):
    out = str(out).strip()
    lines = [line.strip() for line in out.splitlines() if line.strip()]

    if is_plan(out) and lines:
        last_line = lines[-1]
        if len(lines) > 1 and is_action(last_line):
            plan = "\n".join(lines[:-1]).strip()
            return plan, last_line
        return out, None

    if is_action(out):
        return None, out

    return None, None

def trim_session(session):
    canonical_session = [session[0]]
    for message in session[1:]:
        if message["role"] != "assistant":
            canonical_session.append(message)
            continue

        plan, action = normalize_output(message["content"])
        if plan:
            canonical_session.append({"role": "assistant", "content": plan})
        if action:
            canonical_session.append({"role": "assistant", "content": action})
        if not plan and not action:
            canonical_session.append(message)

    system_message = canonical_session[0]
    plan_messages = [
        message for message in canonical_session[1:]
        if message["role"] == "assistant" and is_plan(message["content"])
    ]

    latest_action_index = None
    for index in range(len(canonical_session) - 1, 0, -1):
        message = canonical_session[index]
        if message["role"] == "assistant" and is_action(message["content"]):
            latest_action_index = index
            break

    if latest_action_index is None:
        session[:] = [system_message, *plan_messages]
        return

    latest_action_turn = []
    for index in range(latest_action_index - 1, 0, -1):
        if canonical_session[index]["role"] == "user":
            latest_action_turn.append(canonical_session[index])
            break
    latest_action_turn.append(canonical_session[latest_action_index])

    session[:] = [system_message, *plan_messages, *latest_action_turn]

def brain(image_bytes, session=None, api_key=api_key):
    # Initialize a new session if none is provided
    if session is None:
        session = [{"role": "system", "content": systemprompt}]
    
    img = base64.b64encode(image_bytes).decode()
    
    # Append current turn
    session.append({
        "role": "user",
        "content": [
            {"type": "text", "text": "based on the image, what is the next"
            "action the bot should take to reach its goal? then a single "
            "function call, or when starting a new task or subtask, make a plan by "
            "starting the output with 'plan:'. dont have a plan and a function call. when done with the main task, stop th bot"},
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

    plan, action = normalize_output(out)
    if plan:
        session.append({"role": "assistant", "content": plan})
    if action:
        session.append({"role": "assistant", "content": action})
    if not plan and not action:
        session.pop()
        return out, session

    trim_session(session)

    return action or plan, session
