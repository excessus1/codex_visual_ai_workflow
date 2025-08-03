import shutil
import logging
from pathlib import Path
from .utils import emit_status


def load_config(path):
    import json
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
