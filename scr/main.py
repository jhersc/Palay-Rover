import cv2
from camera.camera import Camera
from motors.motor import DualMotorController

cam = Camera()
motor = DualMotorController()

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

motor.forward(0.3)

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = detector.detectMarkers(gray)

        if ids is not None:
            detected_ids = ids.flatten()

            if 0 in detected_ids:
                print(">> ID 0 detected: STOP ")
                motor.stop()
                motor.turn_right(0.3)

            elif 1 in detected_ids:
                print(">> ID 1 detected: STOP + LEFT TURN")
                motor.stop()
                motor.turn_left(0.3)
            elif 2 in detected_ids:
                print(">> ID 2 detected: STOP + RIGHT TURN")
                motor.stop()
                motor.turn_right(0.3)

            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        cv2.imshow("RiceRaker Feed", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == 27:
            break
        elif key == ord('s'):
            print("EMERGENCY STOP")
            motor.stop()


except KeyboardInterrupt:
    print("\nManual stop.")

finally:
    motor.stop()
    cv2.destroyAllWindows()