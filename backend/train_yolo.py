import os
import json
from ultralytics import YOLO
import yaml
from .utils import emit_status, ensure_dir


def run_training(cfg):
    model_path = cfg['model']
    data = cfg['data']
    output = cfg['output']
    epochs = cfg.get('epochs', 100)
    batch = cfg.get('batch', 16)
    imgsz = cfg.get('imgsz', 640)

    emit_status('start', action='train', model=model_path, data=data)

    ensure_dir(output)
    project = os.path.dirname(output)
    name = os.path.basename(output)

    model = YOLO(model_path)

    with open(data, 'r') as f:
        data_yaml = yaml.safe_load(f)

    class_map = {str(i): name for i, name in enumerate(data_yaml['names'])}
    source_classmap_path = os.path.join(os.path.dirname(data), "class_map.json")
    with open(source_classmap_path, "w") as f:
        json.dump(class_map, f, indent=2)
    emit_status('class_map_saved', path=source_classmap_path)

    class_map_final_path = os.path.join(output, "class_map.json")

    model.train(
        data=data,
        epochs=epochs,
        batch=batch,
        imgsz=imgsz,
        project=project,
        name=name,
        device=0,
    )

    with open(class_map_final_path, "w") as f:
        json.dump(class_map, f, indent=2)
    emit_status('class_map_copied', path=class_map_final_path)

    emit_status('complete', action='train')
