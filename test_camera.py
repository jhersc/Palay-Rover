from camera import Camera
import cv2

cam = Camera()

while True:
    ret, frame = cam.read()

    if not ret:
        print("❌ Frame failed")
        break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()