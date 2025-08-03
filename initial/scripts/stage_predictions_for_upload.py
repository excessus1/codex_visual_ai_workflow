import sys
import json
import logging
import os
from pathlib import Path
from datetime import datetime
from backend.stage_predictions_for_upload import stage_predictions

logs_dir = Path(os.getenv("DATA_DIR", ".")) / "logs" / "image_merge"
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / f"stage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(),
    ]
)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python stage_predictions_for_upload.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path, 'r') as f:
        cfg = json.load(f)
    stage_predictions(cfg)
