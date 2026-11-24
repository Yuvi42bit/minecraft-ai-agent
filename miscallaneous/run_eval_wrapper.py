
from tools_v2 import *
def run(text):
    try:
        text = text.strip()
        eval(text)
    except Exception as exc:
        print(exc)