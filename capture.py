"""Save frames from the ESP32-CAM for training. Usage: python capture.py <camera-ip> <folder-name>
Folder is created under mydata/. Press SPACE to save a frame, A to auto-save 1 frame/sec on/off, q to quit.
Tip: use folder names like 'bottle', 'can', 'background' (frames with NO waste: teaches 'nothing here')."""
import sys, time, pathlib

import cv2

ip, name = sys.argv[1], sys.argv[2]
out = pathlib.Path(__file__).parent / "mydata" / name
out.mkdir(parents=True, exist_ok=True)
n = len(list(out.glob("*.jpg")))
cap = cv2.VideoCapture(f"http://{ip}:81/stream")
auto, last = False, 0.0
while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    now = time.time()
    if auto and now - last >= 1:
        cv2.imwrite(str(out / f"{name}_{n:04d}.jpg"), frame); n += 1; last = now
    show = frame.copy()
    cv2.putText(show, f"{name}: {n} saved  {'AUTO' if auto else ''}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("capture", show)
    k = cv2.waitKey(1)
    if k == ord("q"):
        break
    if k == ord("a"):
        auto = not auto
    if k == ord(" "):
        cv2.imwrite(str(out / f"{name}_{n:04d}.jpg"), frame); n += 1
cap.release()
