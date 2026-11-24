import base64
import os
import re
import requests
from systemprompt import systemprompt

try:
    from dotenv import load_dotenv
except ImportError:  # e.g. in the cloud, where there's no .env anyway
    def load_dotenv(*args, **kwargs):
        return False

# Load OPENROUTER_API_KEY from the .env file next to this script
# (a real environment variable with the same name takes priority).
# In Claude Code cloud there is no key here: a network secret adds it to
# requests to openrouter.ai automatically, so we send no Authorization header.
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key and os.environ.get("CLAUDE_CODE_REMOTE") != "true":
    print("Warning: OPENROUTER_API_KEY is not set. Put OPENROUTER_API_KEY=your-key "
          "in a .env file in the project folder.")


def _headers(key):
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    return headers

MODEL = "inclusionai/ling-3.0-flash-vl"
reasoning = "low"  # "none" turns reasoning off; for this model every other level behaves the same
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MAX_PLANS = 3          # how many recent plans the model keeps seeing
MAX_ACTION_MESSAGES = 2  # last user turn + last action reply

ACTION_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*\(.*\)\s*$")


def is_plan(text):
    return str(text).strip().lower().startswith("plan:")


def is_action(text):
    text = str(text).strip()
    return text.lower() in ("break", "break()") or bool(ACTION_RE.match(text))


def clean_output(out):
    """Strip code fences / backticks the model sometimes wraps answers in."""
    out = str(out).strip()
    out = re.sub(r"^```[a-zA-Z]*\s*", "", out)
    out = re.sub(r"\s*```$", "", out)
    return out.strip().strip("`").strip()


def split_output(out):
    """Return (plan, action). A reply can be a plan, an action, or a plan
    whose last line is an action."""
    out = clean_output(out)
    lines = [line.strip().strip("`") for line in out.splitlines() if line.strip()]
    if not lines:
        return None, None

    if is_plan(out):
        if len(lines) > 1 and is_action(lines[-1]):
            return "\n".join(lines[:-1]), lines[-1]
        return out, None

    # Not a plan: use the last line that looks like an action.
    for line in reversed(lines):
        if is_action(line):
            return None, line
    return None, None


def trim_session(session):
    """Keep the system prompt, the last few plans, and the most recent turn."""
    system = session[0]
    rest = session[1:]

    plans = [m for m in rest if m["role"] == "assistant" and is_plan(m["content"])]
    others = [m for m in rest if not (m["role"] == "assistant" and is_plan(m["content"]))]

    keep_plans = plans[-MAX_PLANS:]
    keep_others = others[-MAX_ACTION_MESSAGES:]
    keep_ids = {id(m) for m in keep_plans + keep_others}

    # Preserve original ordering.
    return [system] + [m for m in rest if id(m) in keep_ids]


def brain(image_bytes, session, prompt, api_key=api_key):
    """Returns (plan, action, session). plan/action may be None."""
    if session is None:
        session = [{"role": "system", "content": systemprompt}]

    img = base64.b64encode(image_bytes).decode()

    session.append({
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}},
        ],
    })

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=_headers(api_key),
            json={"model": MODEL, "messages": session, "reasoning": {"effort": reasoning}},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        out = data["choices"][0]["message"]["content"] or ""
    except (requests.exceptions.RequestException, KeyError, IndexError, ValueError) as e:
        print(f"API request failed: {e}")
        session.pop()  # drop the user turn we just added
        return None, None, session

    plan, action = split_output(out)
    if plan is None and action is None:
        print("brain (unusable reply):", out)

    # Store the plan and action as separate messages so trimming works.
    if plan:
        session.append({"role": "assistant", "content": plan})
    if action:
        session.append({"role": "assistant", "content": action})
    if not plan and not action:
        session.append({"role": "assistant", "content": out})

    session = trim_session(session)
    return plan, action, session
