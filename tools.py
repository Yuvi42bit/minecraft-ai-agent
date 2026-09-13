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

def forward():
    keyboard.press('w')

def backward():
    keyboard.press('s')

def left():
    keyboard.press('a')

def right():
    keyboard.press('d')

def inventory():
    tap_key('e')

def move_mouse(dx, dy):
    mouse.move(int(dx), int(dy))

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

def safe_release(key):
    try:
        keyboard.release(key)
    except:
        pass
def stop():
    safe_release('w')
    safe_release('s')
    safe_release('a')
    safe_release('d')
    mouse.release(Button.left)
