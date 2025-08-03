# scripts/train_yolo.py

import os
import sys
import json
from ultralytics import YOLO
import yaml

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def run_training(cfg):
    model_path = cfg['model']
    data = cfg['data']
    output = cfg['output']
    epochs = cfg.get('epochs', 100)
    batch = cfg.get('batch', 16)
    imgsz = cfg.get('imgsz', 640)

    ensure_dir(output)

    project = os.path.dirname(output)
    name = os.path.basename(output)

    print(f"[INFO] Starting training...\nModel: {model_path}\nData: {data}\nOutput: {output}\nEpochs: {epochs}\nBatch: {batch}\nImg Size: {imgsz}\n")

    model = YOLO(model_path)

#####Create Class Mappings
    # Load and save class map from data.yaml
    with open(data, 'r') as f:
        data_yaml = yaml.safe_load(f)

    class_map = {str(i): name for i, name in enumerate(data_yaml['names'])}

    # Save to source (next to model config)
    source_classmap_path = os.path.join(os.path.dirname(data), "class_map.json")
    with open(source_classmap_path, "w") as f:
        json.dump(class_map, f, indent=2)

    # Temp: hold until success
    class_map_final_path = os.path.join(output, "class_map.json")
    print(f"[INFO] Saved class map: {source_classmap_path}")

###############


    model.train(
        data=data,
        epochs=epochs,
        batch=batch,
        imgsz=imgsz,
        project=project,
        name=name,
        device=0
    )

    # Save again in final output
    with open(class_map_final_path, "w") as f:
        json.dump(class_map, f, indent=2)
    print(f"[INFO] Class map copied to output: {class_map_final_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 train_yolo.py <config_file.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    if not os.path.isfile(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        cfg = json.load(f)

    run_training(cfg)

if __name__ == "__main__":
    main()
