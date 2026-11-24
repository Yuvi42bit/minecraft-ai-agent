import mss
import numpy as np
import cv2

# 320x180 was too small for the model to see blocks, items or the hotbar.
FRAME_SIZE = (960, 540)
JPEG_QUALITY = 80


def get_frame_bytes():
    with mss.mss() as sct:
        monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
        screenshot = sct.grab(monitor)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    frame = cv2.resize(frame, FRAME_SIZE, interpolation=cv2.INTER_AREA)
    success, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
    if not success:
        raise RuntimeError("Failed to encode screenshot")
    return encoded.tobytes()
