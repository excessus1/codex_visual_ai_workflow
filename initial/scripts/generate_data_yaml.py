# scripts/generate_data_yaml.py

import os
import sys
import json
from pathlib import Path
from backend.generate_data_yaml import generate_data_yaml
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

    data_dir = Path(os.getenv("DATA_DIR", "."))
    log_path = setup_logging(data_dir / "logs" / "data_yaml")
    print(f"[INFO] Log written to {log_path}\n")

    generate_data_yaml(cfg)


if __name__ == "__main__":
    main()
