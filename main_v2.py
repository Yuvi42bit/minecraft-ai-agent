import ctypes
import time
import keyboard
from brain import brain
from screencapture_v2 import get_frame_bytes
from run import run
from tools_v2 import stop
from getxt import getxt

STOP_KEY = 'k'
RETRY_SECONDS = 3

prompty = getxt("loopro.txt")
if not prompty:
    raise SystemExit("whoever coded this is an idiotic monkey "
                     "with a degree from the university of moronland, "
                     "please fix the code and add a prompt (loopro.txt is empty)")

# Pressing k at any moment (even mid-API-call) stops the bot.
stop_requested = False


def request_stop():
    global stop_requested
    stop_requested = True
    stop()


keyboard.add_hotkey(STOP_KEY, request_stop)


def foreground_title():
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def minecraft_focused():
    # The game window is e.g. "Minecraft 26.3 - Singleplayer".
    # (Don't match the launcher, or VS Code with "minecraft" in the folder name.)
    title = foreground_title()
    return title.startswith("Minecraft") and "Launcher" not in title


# Key presses only reach the window in front, so wait for Minecraft.
print("Click into the Minecraft game window to start.")
print("If the pause menu is open, click 'Back to Game'. (Tip: press F3+P in-game "
      "so Minecraft stops pausing when it loses focus.)")
while not minecraft_focused() and not stop_requested:
    time.sleep(0.2)
time.sleep(1)  # give you a moment to close the pause menu

print(f"Minecraft AI started. Press {STOP_KEY} to stop.")
session = None
notes = ""  # text from the last script (e.g. recipes()), sent with the next screenshot
try:
    while not stop_requested:
        try:
            image_bytes = get_frame_bytes()
            plan, action, session = brain(image_bytes, session, prompty, notes)
            if plan is not None or action is not None:
                notes = ""  # delivered; on an API error keep it for the retry
            if stop_requested:
                break

            if plan is None and action is None:
                time.sleep(RETRY_SECONDS)  # API error or unusable reply
                continue

            if plan:
                print("plan:", plan)
            if action:
                print("action:", action)
                if action.lower() in ("break", "break()"):
                    print("Goal reached, stopping Minecraft AI...")
                    break
                if not minecraft_focused():
                    # Don't type into whatever other window is in front.
                    stop()
                    print(f"Skipped {action}: Minecraft isn't the focused window "
                          f"(focused: {foreground_title()!r}).")
                    continue
                notes = run(action)
        except Exception as e:
            print("Error:", e)
            time.sleep(1)
finally:
    stop()
    keyboard.unhook_all_hotkeys()
    print("Minecraft AI stopped.")
