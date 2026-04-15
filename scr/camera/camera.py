import cv2

try:
    from picamera2 import Picamera2
    USE_PI = True
except ImportError:
    USE_PI = False


class Camera:
    def __init__(self):
        if USE_PI:
            print("Using Raspberry Pi Camera (640x480)")

            self.cam = Picamera2()

            config = self.cam.create_preview_configuration(
                main={"size": (640, 480)}
            )

            self.cam.configure(config)
            self.cam.start()

        else:
            print("Using Laptop Webcam")

            self.cam = cv2.VideoCapture(0)

            if not self.cam.isOpened():
                raise RuntimeError("Webcam not accessible")

            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def read(self):
        if USE_PI:
            frame = self.cam.capture_array()
            return True, frame
        else:
            return self.cam.read()

    def release(self):
        if not USE_PI:
            self.cam.release()