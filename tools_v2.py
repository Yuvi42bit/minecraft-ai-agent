from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time

mouse = MouseController()
keyboard = KeyboardController()

TAP_SECONDS = 0.05

def tap_key(key):
    keyboard.press(key)
    time.sleep(TAP_SECONDS)
    keyboard.release(key)

def hold_key(key, duration):
    """Helper function to hold a key for a specific duration"""
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)



# --- Continuous Movement (Requires stop() to be called) ---
def forward():
    keyboard.press('w')

def backward():
    keyboard.press('s')
def jump():
    keyboard.press(Key.space)

def left():
    keyboard.press('a')

def right():
    keyboard.press('d')

def stop():
    """Releases all movement keys and mouse buttons."""
    safe_release('w')
    safe_release('s')
    safe_release('a')
    safe_release('d')
    safe_release(Key.space)
    try:
        mouse.release(Button.left)
        mouse.release(Button.right)
    except Exception:
        pass

def safe_release(key):
    try:
        keyboard.release(key)
    except Exception:
        pass

# --- Actions ---
def inventory():
    tap_key('e')

def move_mouse(dx, dy):
    mouse.move(int(dx*10), int(dy*10))

def mine():
    mouse.press(Button.left)

def attack():
    mouse.click(Button.left)

def place_or_interact():
    mouse.click(Button.right)

def hotbar_navigate(slot_num):
    slot_num = int(slot_num)
    if not 1 <= slot_num <= 9:
        raise ValueError("hotbar slot must be between 1 and 9")
    tap_key(str(slot_num))
