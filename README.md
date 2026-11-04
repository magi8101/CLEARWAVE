# CLEARWAVE

Floating-waste detection for lakes and sea. An ESP32-CAM streams video over WiFi to a PC, where a fine-tuned YOLO26 model detects waste live. Built to mount on a small rover/boat rig (ESP32, L298N, TT motors).

## What's here

| Path | What it does |
|---|---|
| `CameraWebServer/CameraWebServer/` | ESP32-CAM firmware (AI Thinker). WiFi auto-retry, `esp32cam.local` via mDNS |
| `camtest/` | Minimal camera test, no WiFi (serial output + flash LED) |
| `yolo_stream.py` | Live MJPEG stream from the camera into YOLO |
| `train_waste.py` | Fine-tune YOLO26s on a floating-waste dataset |
| `stoplight.py` | OpenCV red/green light detector (no ML) |
| `runs/detect/waste/weights/best.pt` | Trained model |

## 1. Flash the camera

Needs `arduino-cli` and the ESP32 Arduino core **2.0.17**.

1. In `CameraWebServer.ino`, set `ssid` and `password` (the repo has a placeholder password).
2. Flash:

```bash
cd CameraWebServer/CameraWebServer
FQBN="esp32:esp32:esp32:PSRAM=enabled,PartitionScheme=huge_app,FlashMode=dio"
arduino-cli compile --fqbn "$FQBN" .
arduino-cli upload -p /dev/ttyUSB0 --fqbn "$FQBN" .
```

The camera joins your WiFi and answers at `http://esp32cam.local` (IP can change, the name doesn't). Your PC must be on the same network.

## 2. Live detection

```bash
pip install ultralytics opencv-python
curl "http://esp32cam.local/control?var=framesize&val=8"   # VGA (resets on reboot)
python yolo_stream.py esp32cam.local runs/detect/waste/weights/best.pt
```

Press `q` to quit. It reconnects if the stream drops. The stream allows one client at a time.

## 3. Train

```bash
python train_waste.py <path/to/data.yaml> [epochs]
```

Trained on a [Mendeley floating-waste dataset](https://data.mendeley.com/) (CC BY 4.0, YOLO format; 750 train / 315 val / 158 test images), RTX 3050 6 GB, 60 epochs, batch 8.

## Current results

Validation set, 2 classes:

| Class | mAP50 | mAP50-95 |
|---|---|---|
| floating_waste | 0.40 | 0.12 |
| river_vegetation | 0.28 | 0.08 |
| all | 0.34 | 0.10 |

Known limits:
- Only two classes, so it cannot name waste types (bottle, can, bag).
- Domain gap: the dataset photos are sharper than ESP32-CAM frames, so live accuracy is lower than the table.
- Unknown objects get forced into one of the two classes.

## Next

- Dataset with waste-type classes (bottle, can, bag, wrapper, carton).
- Add labeled frames from the real camera, including empty-background frames.
- Export to ONNX and run in the browser with onnxruntime-web.

## Troubleshooting

- **Brownout resets / no WiFi:** weak USB power or cable. Use a good 5 V supply.
- **Serial permission denied:** `sudo chmod 666 /dev/ttyUSB0` (resets on replug) or add yourself to `dialout`.
- **Camera unreachable:** laptop and camera must be on the same WiFi.

## ONNX model

`models/clearwave-4class.onnx` (YOLO26s, input 1x3x640x640 RGB 0-1, output 1x8x8400 = 4 box + 4 class scores per candidate, needs NMS). Classes in `models/classes.txt`. Val mAP50 0.87 on a small 40-image set; weaker on real ESP32-CAM frames.
