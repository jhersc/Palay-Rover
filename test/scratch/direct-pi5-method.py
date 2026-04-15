import cv2
import time
import numpy as np
from picamera2 import Picamera2
from gpiozero import PWMOutputDevice, DigitalOutputDevice

# --- 1. MOTOR SETUP ---
motor_pwm = PWMOutputDevice(17, frequency=100) 
motor_dir = DigitalOutputDevice(27)

SLOW_SPEED = 0.15 
STOP_SPEED = 0.0

current_motor_state = STOP_SPEED 

def set_motor(speed):
    motor_dir.value = 0
    motor_pwm.value = speed

# --- 2. CAMERA SETUP ---
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# --- 3. ARUCO SETUP ---
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

print("--- RiceRaker Latching State Test ---")
print("Show ID 0: START (will keep running even if hidden)")
print("Show ID 1: STOP")

try:
    while True:
        raw_frame = picam2.capture_array()
        frame = cv2.cvtColor(raw_frame, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, rejected = detector.detectMarkers(gray)

        if ids is not None:
            detected_ids = ids.flatten()
            
            if 1 in detected_ids:
                print(">> ID 1 detected: Latching STOP")
                current_motor_state = STOP_SPEED
            elif 0 in detected_ids:
                print(">> ID 0 detected: Latching START")
                current_motor_state = SLOW_SPEED
            
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        set_motor(current_motor_state)
        
        status_text = "RUNNING" if current_motor_state > 0 else "STOPPED"
        cv2.putText(frame, f"Motor: {status_text}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("RiceRaker Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nManual stop.")

finally:
    set_motor(0)
    picam2.stop()
    cv2.destroyAllWindows()