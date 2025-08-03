import argparse
import json
import os
from ultralytics import YOLO
from datetime import datetime
import subprocess


def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)


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

    model = YOLO(model_path)
    model.predict(source=source, save=True, save_txt=True, conf=conf, project=project, name=name, device=0)

    if cfg.get('convert_to_ls'):
        converter_path = os.path.join(os.path.dirname(__file__), 'convert_yolo_to_ls.py')
        if os.path.exists(converter_path):
            print(f"\n[INFO] Running post-process conversion: {converter_path}\n")
            subprocess.run(['python', converter_path, '--source', os.path.join(output, 'labels')])
        else:
            print("[WARN] convert_yolo_to_ls.py not found. Skipping conversion.")


def run_training(cfg):
    model_path = cfg['model']
    data_yaml = cfg['data']
    output = cfg['output']
    epochs = cfg.get('epochs', 100)
    batch = cfg.get('batch', 16)
    imgsz = cfg.get('imgsz', 640)

    ensure_dir(output)

    project = os.path.dirname(output)
    name = os.path.basename(output)

    model = YOLO(model_path)
    model.train(data=data_yaml, epochs=epochs, batch=batch, imgsz=imgsz, project=project, name=name, save=True, plots=True)


def main():
    parser = argparse.ArgumentParser(description="Run YOLOv8 training or prediction from JSON config")
    parser.add_argument('--config', required=True, help="Path to JSON config file")
    args = parser.parse_args()

    config = load_config(args.config)
    mode = config.get('mode')

    if mode == 'predict':
        run_prediction(config)
    elif mode == 'train':
        run_training(config)
    else:
        raise ValueError("'mode' must be either 'predict' or 'train'")


if __name__ == '__main__':
    main()
