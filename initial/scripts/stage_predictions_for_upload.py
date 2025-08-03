import os
import shutil
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"logs/image_merge/stage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def stage_predictions(config_path):
    config = load_config(config_path)

    prediction_dir = Path(config['prediction_dir'])
    labels_dir = prediction_dir / 'labels'
    dest_root = Path(config['destination'])
    images_dest = dest_root / 'images'
    labels_dest = dest_root / 'labels'

    ensure_dir(images_dest)
    ensure_dir(labels_dest)

    count = 0
    skipped = 0

    for label_file in labels_dir.glob('*.txt'):
        image_file = prediction_dir / label_file.name.replace('.txt', '.jpg')

        if not image_file.exists():
            logging.warning(f"Missing image for label: {label_file.name}")
            skipped += 1
            continue

        shutil.copy2(image_file, images_dest / image_file.name)
        shutil.copy2(label_file, labels_dest / label_file.name)
        logging.info(f"Staged: {image_file.name} and {label_file.name}")
        count += 1

    logging.info(f"[DONE] Staged {count} image/label pairs. Skipped: {skipped}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python stage_predictions_for_upload.py <config.json>")
        sys.exit(1)

    stage_predictions(sys.argv[1])
