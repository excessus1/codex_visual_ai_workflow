# scripts/collect_images.py

import os
import sys
import json
import logging
from pathlib import Path
from backend.collect_images import collect_images, setup_logger


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 collect_images.py <config_file.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    if not os.path.isfile(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r") as f:
        cfg = json.load(f)

    data_dir = Path(os.getenv("DATA_DIR", "."))
    log_dir = data_dir / "logs" / "image_merge"
    log_path = setup_logger(log_dir)

    logging.info("=== Starting Image Collection ===")
    logging.info(f"Config: {config_path}")
    logging.info(f"Sources: {cfg['sources']}")
    logging.info(f"Destination: {cfg['destination']}")
    logging.info(f"Rename scheme: {cfg.get('rename_scheme', 'source_prefix')}")
    logging.info(f"Delete missing in sources: {cfg.get('delete_missing_in_sources', False)}")

    collect_images(cfg)

    logging.info("=== Collection Complete ===")
    print(f"[INFO] Log written to {log_path}")


if __name__ == "__main__":
    main()
