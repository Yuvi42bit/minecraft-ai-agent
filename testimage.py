import cv2
import numpy as np

from screencapture import get_frame_bytes


def main():
    image_bytes = get_frame_bytes()
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if frame is None:
        raise RuntimeError("Failed to decode screenshot")

    cv2.imshow("Screenshot", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
