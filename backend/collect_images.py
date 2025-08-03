import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from filecmp import cmp
from .utils import emit_status, set_status_callback


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def setup_logger(log_dir: Path):
    ensure_dir(log_dir)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"collect_{now}.log"
    logging.basicConfig(
        filename=log_path,
        filemode='w',
        format='[%(asctime)s] %(message)s',
        level=logging.INFO,
    )
    return log_path


def get_unique_name(dest_dir, original_name, source_prefix, method):
    base = Path(original_name).stem
    ext = Path(original_name).suffix.lower()

    if method == "source_prefix":
        return f"{source_prefix}_{base}{ext}"
    elif method == "timestamp_hash":
        now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"{now}_{base}{ext}"
    elif method == "sequential":
        i = 0
        new_name = f"{base}{ext}"
        while (Path(dest_dir) / new_name).exists():
            new_name = f"{base}_{i}{ext}"
            i += 1
        return new_name
    else:
        raise ValueError(f"Unknown rename_scheme: {method}")


def collect_images(cfg, db=None):
    sources = cfg["sources"]
    dest_dir = Path(cfg["destination"])
    rename_scheme = cfg.get("rename_scheme", "source_prefix")
    rename_only_on_conflict = cfg.get("rename_only_on_conflict", False)
    delete_missing = cfg.get("delete_missing_in_sources", False)
    valid_exts = {ext.lower() for ext in cfg.get("extensions", [".jpg", ".jpeg", ".png"])}

    ensure_dir(dest_dir)
    seen_files = set()
    total, copied, renamed, skipped = 0, 0, 0, 0
    emit_status('start', action='collect_images', sources=len(sources))

    if db is not None:
        db.logActivity({
            'action': 'collect_images',
            'details': json.dumps({'config': cfg}),
            'status': 'running',
        })

        def _cb(event: str, data: dict) -> None:
            if event == 'complete':
                final = {
                    'total': total,
                    'copied': copied,
                    'renamed': renamed,
                    'skipped': skipped,
                    'destination': str(dest_dir),
                }
                db.logActivity({
                    'action': 'collect_images_complete',
                    'details': json.dumps(final),
                    'status': 'complete',
                })

        set_status_callback(_cb)

    for source in sources:
        source_path = Path(source)
        prefix = source_path.name
        if not source_path.exists():
            logging.warning(f"Source not found: {source_path}")
            continue

        for file in source_path.iterdir():
            if file.suffix.lower() not in valid_exts or not file.is_file():
                continue

            base = file.stem
            ext = file.suffix.lower()
            dest_file = dest_dir / f"{base}{ext}"

            if not dest_file.exists():
                shutil.copy(file, dest_file)
                seen_files.add(dest_file.name.lower())
                logging.info(f"[ADD] {file} → {dest_file}")
                copied += 1
                emit_status('copied', file=str(file))
            elif cmp(file, dest_file, shallow=False):
                seen_files.add(dest_file.name.lower())
                logging.info(f"[SKIP] Identical: {file.name}")
                skipped += 1
                emit_status('skipped', file=str(file))
            else:
                if rename_only_on_conflict:
                    new_name = get_unique_name(dest_dir, file.name, prefix, rename_scheme)
                    new_dest = dest_dir / new_name
                    shutil.copy(file, new_dest)
                    seen_files.add(new_dest.name.lower())
                    logging.info(f"[RENAME] Conflict: {file.name} → {new_name}")
                    renamed += 1
                    emit_status('renamed', file=str(file), new_name=new_name)
                else:
                    shutil.copy(file, dest_file)
                    seen_files.add(dest_file.name.lower())
                    logging.info(f"[OVERWRITE] {file} → {dest_file}")
                    copied += 1
                    emit_status('overwritten', file=str(file))

            total += 1

    if delete_missing:
        for existing_file in dest_dir.iterdir():
            if existing_file.is_file() and existing_file.name.lower() not in seen_files:
                existing_file.unlink()
                logging.info(f"[DELETE] Removed missing source file: {existing_file.name}")
                emit_status('deleted', file=str(existing_file))

    emit_status('complete', action='collect_images', total=total, copied=copied, renamed=renamed, skipped=skipped)
    if db is not None:
        set_status_callback(None)
    return {
        'total': total,
        'copied': copied,
        'renamed': renamed,
        'skipped': skipped,
    }


def run(config_path: str, db=None) -> None:
    """Entry point used by CLI and other callers.

    Loads the JSON config, sets up logging, and invokes :func:`collect_images`.
    """
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

    collect_images(cfg, db=db)

    logging.info("=== Collection Complete ===")
    print(f"[INFO] Log written to {log_path}")


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m backend.collect_images <config.json>")
        sys.exit(1)
    run(argv[0])


if __name__ == "__main__":
    main()
