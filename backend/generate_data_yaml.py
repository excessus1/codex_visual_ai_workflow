import json
from pathlib import Path
import yaml
import logging
from .utils import emit_status


def ensure_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def generate_data_yaml(cfg):
    classes_path = Path(cfg["classes_file"])
    output_path = Path(cfg["output_file"])
    train_path = Path(cfg["train_images"])
    val_path = Path(cfg["val_images"])

    emit_status('start', action='generate_data_yaml')

    if not classes_path.exists():
        logging.error(f"Classes file not found: {classes_path}")
        emit_status('error', message=f"Classes file not found: {classes_path}")
        return

    with open(classes_path, "r") as f:
        classes = [line.strip() for line in f if line.strip()]

    data = {
        "train": str(train_path.resolve()),
        "val": str(val_path.resolve()),
        "nc": len(classes),
        "names": classes,
    }

    ensure_dir(output_path)
    with open(output_path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

    emit_status('complete', action='generate_data_yaml', classes=len(classes), output=str(output_path))
    return data
