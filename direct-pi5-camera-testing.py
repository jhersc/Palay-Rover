import cv2
import time
import numpy as np
from picamera2 import Picamera2

# --- 1. SETUP CAMERA ---
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# --- 2. ARUCO SETUP ---
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

print("--- RiceRaker VISION ONLY Test ---")

try:
    while True:
        raw_frame = picam2.capture_array()

        frame = cv2.cvtColor(raw_frame, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, rejected = detector.detectMarkers(gray)

        if ids is not None:
            detected_ids = ids.flatten()
            print(f"Detected: {detected_ids}")
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        else:
            print("Scanning...", end="\r")

        cv2.imshow("RiceRaker Feed", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    print("Closing camera and windows...")
    picam2.stop()
    cv2.destroyAllWindows()