# convert_yolo_to_ls.py

import sys
import json
from backend.convert_yolo_to_ls import convert_yolo_to_ls


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_yolo_to_ls.py <config.json>")
        exit(1)

    config_path = sys.argv[1]
    with open(config_path, 'r') as f:
        cfg = json.load(f)

    convert_yolo_to_ls(cfg)
