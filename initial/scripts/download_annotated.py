# scripts/download_annotated.py

import os
import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from backend.download_annotated import download_annotated


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def setup_logging(log_dir):
    ensure_dir(log_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path(log_dir) / f"download_annotated_{timestamp}.log"
    logging.basicConfig(
        filename=log_path,
        filemode='w',
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    )
    return log_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 download_annotated.py <config_file.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    if not os.path.isfile(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r") as f:
        cfg = json.load(f)

    labels_dir = cfg.get("labels_dir")
    images_dir = cfg.get("images_dir")
    output_dir = cfg.get("output_dir")

    if not all([labels_dir, images_dir, output_dir]):
        print("[ERROR] Config must include 'labels_dir', 'images_dir', and 'output_dir'.")
        sys.exit(1)

    log_path = setup_logging("logs/download")
    print(f"[INFO] Log written to {log_path}\n")
    download_annotated(cfg)


if __name__ == "__main__":
    main()
