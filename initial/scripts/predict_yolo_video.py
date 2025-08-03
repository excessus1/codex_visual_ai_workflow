# scripts/predict_yolo_image.py

import os
import sys
import json
from ultralytics import YOLO
import logging
from glob import glob

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/predict_yolo_video.log"),
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

    files = sorted(glob(os.path.join(source, "*.mp4")))  # or filter further if needed
    total_files = len(files)

    for idx, file in enumerate(files, start=1):
        logging.info(f"[{idx}/{total_files}] Starting: {os.path.basename(file)}")

        results = model.predict(
            source=file,
            save=True,
            save_txt=True,
            conf=conf,
            project=project,
            name=name,
            device=0,
            stream=True
        )

        for r in results:
            n_boxes = len(r.boxes) if r.boxes else 0
            logging.info(f"[{idx}/{total_files}] {os.path.basename(file)}: {n_boxes} detections in frame {r.path if hasattr(r, 'path') else '?'}")

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
