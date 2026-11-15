
import time
import keyboard
from brain import brain
from screencapture_v2 import get_frame_bytes
from run import run
from tools_v2 import stop
from getxt import getxt
prompty = getxt("loopro.txt")
for i in range(5):
    print(f"Starting in {5 - i} seconds...")
    time.sleep(1)

print("Minecraft AI started. k to stop.")
session = None
while True:
    try:
        if keyboard.is_pressed('k'):
            print("Stopping Minecraft AI...")
            break

        image_bytes = get_frame_bytes()
        response, session = brain(image_bytes, session, prompty)
        if prompty is None or not prompty.strip():
            print("whoever coded this is an idiotic monkey " \
            "with a degree from the university of moronland, " \
            "please fix the code and add a prompt")
            break
        if response is None:
            continue
        if response.strip() == "break":
            print("Stopping Minecraft AI...")
            stop()
            break
        print("brain:", response)
        if str(response).startswith("plan:"):
            pass
        else:
            print("brain:", response)
            run(response)
    except Exception as e:
        print("Error:", e)
        time.sleep(1)

print("Minecraft AI stopped.")
stop()
