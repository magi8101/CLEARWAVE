"""Fine-tune YOLO26s on a floating-waste dataset (YOLO format, from Roboflow).
Usage: python train_waste.py <path/to/data.yaml> [epochs]
Result: runs/detect/waste/weights/best.pt  -> use with yolo_stream.py <ip> best.pt"""
import sys

import torch
from ultralytics import YOLO

data = sys.argv[1]
epochs = int(sys.argv[2]) if len(sys.argv) > 2 else 60
gpu = torch.cuda.is_available()
print("training on", "GPU" if gpu else "CPU (very slow)")

YOLO("yolo26s.pt").train(  # swap to "yolo11s.pt" to compare
    data=data,
    epochs=epochs,
    imgsz=640,
    batch=8,  # fits RTX 3050 6 GB; lower to 4 if you get an out-of-memory error
    device=0 if gpu else "cpu",
    name="waste",
    patience=15,  # stop early if it stops improving
    workers=2,
)
