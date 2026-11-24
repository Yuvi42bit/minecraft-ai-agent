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
    """Run each command in the script. Returns any text the commands gave back
    (e.g. from recipes()) plus errors, so the AI can see them next turn."""
    results = []
    for com in split_commands(text):
        try:
            out = eval(com)
            if out is not None:
                results.append(str(out))
        except Exception as exc:
            print(exc)
            results.append(f"{com} failed: {exc}")
    return "\n".join(results)
