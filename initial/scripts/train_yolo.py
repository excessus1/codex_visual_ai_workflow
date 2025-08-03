import os
import sys
import json
from backend.train_yolo import run_training


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
