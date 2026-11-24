import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def getxt(file):
    """Read a text file relative to this project folder, so the bot works
    no matter which folder you start it from."""
    with open(os.path.join(BASE_DIR, file), "r", encoding="utf-8") as f:
        return f.read().strip()
