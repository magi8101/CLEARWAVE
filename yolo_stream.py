"""ESP32-CAM MJPEG stream -> YOLO. Usage: python yolo_stream.py <camera-ip> [model]
Press q in the window to quit. Reconnects by itself if the stream drops."""
import sys
import time

import cv2
from ultralytics import YOLO

ip = sys.argv[1]
model = YOLO(sys.argv[2] if len(sys.argv) > 2 else "yolo11n.pt")  # n = fastest; weights auto-download
W, H = 960, 720  # fixed window size, whatever the camera sends

cv2.namedWindow("esp32-cam yolo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("esp32-cam yolo", W, H)

quit_ = False
while not quit_:
    cap = cv2.VideoCapture(f"http://{ip}:81/stream")  # CameraWebServer stream port
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        img = model(frame, conf=0.10, verbose=False)[0].plot()
        cv2.imshow("esp32-cam yolo", cv2.resize(img, (W, H)))
        if cv2.waitKey(1) == ord("q"):
            quit_ = True
            break
    cap.release()
    if not quit_:
        print("stream lost, reconnecting...")
        time.sleep(2)
