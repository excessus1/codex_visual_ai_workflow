import shutil
import logging
import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from .utils import emit_status


def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def stage_predictions(cfg):
    prediction_dir = Path(cfg['prediction_dir'])
    labels_dir = prediction_dir / 'labels'
    dest_root = Path(cfg['destination'])
    images_dest = dest_root / 'images'
    labels_dest = dest_root / 'labels'

    ensure_dir(images_dest)
    ensure_dir(labels_dest)

    count = 0
    skipped = 0
    emit_status('start', action='stage_predictions')

    for label_file in labels_dir.glob('*.txt'):
        image_file = prediction_dir / label_file.name.replace('.txt', '.jpg')
        if not image_file.exists():
            logging.warning(f"Missing image for label: {label_file.name}")
            skipped += 1
            emit_status('missing_image', label=str(label_file))
            continue

        shutil.copy2(image_file, images_dest / image_file.name)
        shutil.copy2(label_file, labels_dest / label_file.name)
        logging.info(f"Staged: {image_file.name} and {label_file.name}")
        emit_status('staged', image=image_file.name, label=label_file.name)
        count += 1

    emit_status('complete', action='stage_predictions', staged=count, skipped=skipped)
    return {'staged': count, 'skipped': skipped}


def setup_logging(log_dir: Path) -> Path:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path(log_dir) / f"stage_predictions_{timestamp}.log"
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='[%(levelname)s] %(message)s',
    )
    return log_path


def run(config_path: str) -> None:
    cfg = load_config(config_path)
    data_dir = Path(os.getenv("DATA_DIR", "."))
    log_path = setup_logging(data_dir / "logs" / "image_merge")
    print(f"[INFO] Log written to {log_path}")
    stage_predictions(cfg)


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m backend.stage_predictions_for_upload <config.json>")
        sys.exit(1)
    run(argv[0])


if __name__ == "__main__":
    main()
