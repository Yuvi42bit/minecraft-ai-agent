from tools_v2 import *
#run a script
#example script:
# forward(),wait(1),jump(),wait(0.5),stop()


def split_commands(text):
    """Split on commas that are not inside brackets, so move_mouse(-300, 0)
    stays one command."""
    commands = []
    depth = 0
    current = ""
    for ch in text:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            commands.append(current)
            current = ""
        else:
            current += ch
    commands.append(current)
    return [c.strip() for c in commands if c.strip()]


def run(text):
    for com in split_commands(text):
        try:
            eval(com)
        except Exception as exc:
            print(exc)
