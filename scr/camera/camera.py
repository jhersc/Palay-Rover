import cv2

try:
    from picamera2 import Picamera2
    USE_PI = True
except ImportError:
    USE_PI = False

class Camera:
    def __init__(self):
        if USE_PI:
            print("📷 Using Raspberry Pi Camera")
            self.cam = Picamera2()
            self.cam.start()
        else:
            print("💻 Using Laptop Webcam")
            self.cam = cv2.VideoCapture(0)

            if not self.cam.isOpened():
                raise RuntimeError("❌ Webcam not accessible")

    def read(self):
        if USE_PI:
            frame = self.cam.capture_array()
            return True, frame
        else:
            return self.cam.read()

    def release(self):
        if not USE_PI:
            self.cam.release()