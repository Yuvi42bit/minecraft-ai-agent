import ctypes
import time

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

mouse = MouseController()
keyboard = KeyboardController()

TAP_SECONDS = 0.05


def tap_key(key):
    keyboard.press(key)
    time.sleep(TAP_SECONDS)
    keyboard.release(key)


# --- Continuous actions: they start and keep going until stop() ---
# They stack, e.g. forward() then jump() walks forward while jumping.
def forward():
    keyboard.press('w')


def backward():
    keyboard.press('s')


def left():
    keyboard.press('a')


def right():
    keyboard.press('d')


def jump():
    """Keep jumping. Combine with forward() to climb onto blocks."""
    keyboard.press(Key.space)


def safe_release(key):
    try:
        keyboard.release(key)
    except Exception:
        pass


def stop():
    """Releases all movement keys and mouse buttons."""
    for key in ('w', 's', 'a', 'd', Key.space):
        safe_release(key)
    for button in (Button.left, Button.right):
        try:
            mouse.release(button)
        except Exception:
            pass


# --- Mouse movement that Minecraft actually sees ---
# pynput moves the cursor by setting its position, which Minecraft ignores
# when "Raw Input" is on. SendInput with relative movement works either way.
class _MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong), ("dwExtraInfo", ctypes.c_size_t)]


class _Input(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [("mi", _MouseInput),
                    ("_pad", ctypes.c_byte * 32)]  # big enough for any INPUT kind
    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong), ("u", _U)]


_INPUT_MOUSE = 0
_MOUSEEVENTF_MOVE = 0x0001
_MOUSE_STEPS = 10


def _send_relative(dx, dy):
    inp = _Input(type=_INPUT_MOUSE)
    inp.mi = _MouseInput(dx, dy, 0, _MOUSEEVENTF_MOVE, 0, 0)
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(_Input))


def move_mouse(dx, dy):
    """Turn the camera. Positive dx = right, positive dy = down.
    At default sensitivity, about 600 = a 90 degree turn."""
    dx, dy = int(dx), (int(dy))
    # Split into small steps so big turns are smooth and not dropped.
    sent_x = sent_y = 0
    for i in range(1, _MOUSE_STEPS + 1):
        step_x = dx * i // _MOUSE_STEPS - sent_x
        step_y = dy * i // _MOUSE_STEPS - sent_y
        sent_x += step_x
        sent_y += step_y
        _send_relative(step_x, step_y)
        time.sleep(0.01)


# --- Actions ---
def inventory():
    tap_key('e')


def mine():
    """Start holding left click to break blocks. Continues until stop()."""
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
