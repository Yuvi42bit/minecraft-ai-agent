import mss
import numpy as np
import cv2

if not hasattr(np, "float128"):
    np.float128 = np.float64

def get_frame_bytes():
    with mss.mss() as sct:
        monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        frame = cv2.resize(frame, (320, 180))
        success, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        if not success:
            raise RuntimeError("Failed to encode screenshot")
        return encoded.tobytes()
