import sys
import json
import logging
from datetime import datetime
from backend.stage_predictions_for_upload import stage_predictions

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"logs/image_merge/stage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
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
