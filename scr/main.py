from collections import deque
import cv2

from camera.camera import Camera
from motors.motor import DualMotorController


cam = Camera()
motor = DualMotorController()

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

motor.forward(0.1)

recent_ids = deque(maxlen=10)

try:
    while True:
        ret, frame = cam.read()

        if not ret or frame is None or frame.size == 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = detector.detectMarkers(gray)

        if ids is not None:
            recent_ids.extend(ids.flatten())
        else:
            # optional but important: decay old detections
            recent_ids.clear()

        # decision logic (stable across frames)
        if 0 in recent_ids:
            motor.stop()
            motor.turn_right(0.3)

        elif 1 in recent_ids:
            motor.stop()
            motor.turn_left(0.3)

        elif 2 in recent_ids:
            motor.stop()
            motor.turn_right(0.3)

        # safe drawing
        if ids is not None and frame is not None and frame.size != 0:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        cv2.imshow("RiceRaker Feed", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == 27:
            break
        elif key == ord('s'):
            motor.stop()

except KeyboardInterrupt:
    pass

finally:
    motor.stop()
    cv2.destroyAllWindows()