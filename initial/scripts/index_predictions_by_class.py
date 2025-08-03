# index_predictions_by_class.py

import os
import sys
import json
import argparse
from backend.index_predictions_by_class import index_predictions


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

    index_predictions(cfg)


if __name__ == "__main__":
    main()
