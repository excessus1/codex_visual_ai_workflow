# scripts/generate_data_yaml.py

import sys
import json
from pathlib import Path
import yaml
import logging
from datetime import datetime

def ensure_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

def setup_logging(log_dir):
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path(log_dir) / f"generate_data_yaml_{timestamp}.log"
    logging.basicConfig(
        filename=log_path,
        filemode='w',
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    )
    return log_path

def generate_data_yaml(cfg):
    classes_path = Path(cfg["classes_file"])
    output_path = Path(cfg["output_file"])
    train_path = Path(cfg["train_images"])
    val_path = Path(cfg["val_images"])

    if not classes_path.exists():
        logging.error(f"Classes file not found: {classes_path}")
        sys.exit(1)

    with open(classes_path, "r") as f:
        classes = [line.strip() for line in f if line.strip()]

    data = {
        "train": str(train_path.resolve()),
        "val": str(val_path.resolve()),
        "nc": len(classes),
        "names": classes
    }

    ensure_dir(output_path)
    with open(output_path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

    logging.info(f"Wrote data.yaml with {len(classes)} classes to {output_path}")
    print(f"[INFO] data.yaml created at: {output_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_data_yaml.py <config_file.json>")
        sys.exit(1)

    config_path = Path(sys.argv[1])
    if not config_path.exists():
        print(f"[ERROR] Config not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r") as f:
        cfg = json.load(f)

    log_path = setup_logging("logs/data_yaml")
    print(f"[INFO] Log written to {log_path}\n")

    generate_data_yaml(cfg)

if __name__ == "__main__":
    main()
