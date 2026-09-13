import re
from tools_v2 import (
    forward, backward, jump, left, right, inventory,
    move_mouse, mine, attack, place_or_interact,
    hotbar_navigate, stop
)

actions = {
    "forward": forward,
    "backward": backward,
    "jump": jump,
    "left": left,
    "right": right,
    "inventory": inventory,
    "move_mouse": move_mouse,
    "mine": mine,
    "attack": attack,
    "place_or_interact": place_or_interact,
    "hotbar_navigate": hotbar_navigate,
    "stop": stop
}

ACTION_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*\((.*?)\)\s*$")


def _parse_value(value):
    value = value.strip()
    try:
        num = float(value)
    except ValueError:
        return value
    return int(num) if num.is_integer() else num


def run(text):
    text = str(text).strip()
    match = ACTION_RE.match(text)
    if not match:
        print("Invalid action format:", text)
        return

    func_name = match.group(1)
    raw_params = match.group(2).strip()

    if func_name not in actions:
        print("Unknown action:", func_name)
        return

    args = []
    kwargs = {}
    if raw_params:
        for param in raw_params.split(","):
            if "=" in param:
                name, value = param.split("=", 1)
                kwargs[name.strip()] = _parse_value(value)
            else:
                args.append(_parse_value(param))

    try:
        actions[func_name](*args, **kwargs)
    except TypeError as exc:
        print(f"Bad parameters for {func_name}: args={args}, kwargs={kwargs} ({exc})")
    except ValueError as exc:
        print(f"Invalid value for {func_name}: {exc}")
    except Exception as exc:
        print(f"Unexpected error in {func_name}: {exc}")
