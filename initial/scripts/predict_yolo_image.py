# scripts/predict_yolo_image.py

import os
import sys
import json
from ultralytics import YOLO
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/predict_yolo_image.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def run_prediction(cfg):
    model_path = cfg['model']
    source = cfg['source']
    output = cfg['output']
    conf = cfg.get('conf', 0.25)

    ensure_dir(output)

    project = os.path.dirname(output)
    name = os.path.basename(output)

    print(f"[INFO] Starting prediction...\nModel: {model_path}\nSource: {source}\nOutput: {output}\nConf: {conf}\n")
    model = YOLO(model_path)
    results = model.predict(
        source=source,
        save=True,
        save_txt=True,
        conf=conf,
        project=project,
        name=name,
        device=0,
        stream=True

    )

    for r in results:
        logging.info(f"Processed {r.path} with {len(r.boxes)} detections.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 predict_yolo.py <config_file.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    if not os.path.isfile(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        cfg = json.load(f)

    run_prediction(cfg)

if __name__ == "__main__":
    main()
