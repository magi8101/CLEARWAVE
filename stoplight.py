"""ESP32-CAM stream -> red/green light detector (OpenCV only). Usage: python stoplight.py <camera-ip>
q quits. Tune MIN_AREA / HSV ranges for your light and room."""
import sys

import cv2

MIN_AREA = 150  # px; ignore tiny specks. Raise it if you get false hits.
RANGES = {  # HSV ranges; red wraps around 0 so it has two
    "RED": [((0, 120, 120), (10, 255, 255)), ((170, 120, 120), (180, 255, 255))],
    "GREEN": [((40, 80, 80), (90, 255, 255))],
}
COLOR = {"RED": (0, 0, 255), "GREEN": (0, 255, 0)}

src = int(sys.argv[1]) if sys.argv[1].isdigit() else f"http://{sys.argv[1]}:81/stream"  # 0 = laptop webcam
cap = cv2.VideoCapture(src)
while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (7, 7), 0), cv2.COLOR_BGR2HSV)
    state = "NONE"
    for name, rs in RANGES.items():
        mask = sum(cv2.inRange(hsv, lo, hi) for lo, hi in rs)
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        big = [c for c in cnts if cv2.contourArea(c) > MIN_AREA]
        if big:
            x, y, w, h = cv2.boundingRect(max(big, key=cv2.contourArea))
            cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR[name], 2)
            if name == "RED" or state == "NONE":  # red wins: safer to stop
                state = name
    cv2.putText(frame, state, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("stoplight", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
