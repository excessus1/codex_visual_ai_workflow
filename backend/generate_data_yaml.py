import json
import os
import sys
from pathlib import Path
import yaml
import logging
from datetime import datetime
from .utils import emit_status, ensure_dir


def generate_data_yaml(cfg):
    classes_path = Path(cfg["classes_file"])
    output_path = Path(cfg["output_file"])
    train_path = Path(cfg["train_images"])
    val_path = Path(cfg["val_images"])

    emit_status('start', action='generate_data_yaml')

    if not classes_path.exists():
        logging.error(f"Classes file not found: {classes_path}")
        emit_status('error', message=f"Classes file not found: {classes_path}")
        return

    with open(classes_path, "r") as f:
        classes = [line.strip() for line in f if line.strip()]

    data = {
        "train": str(train_path.resolve()),
        "val": str(val_path.resolve()),
        "nc": len(classes),
        "names": classes,
    }

    ensure_dir(output_path.parent)
    with open(output_path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

    emit_status('complete', action='generate_data_yaml', classes=len(classes), output=str(output_path))
    return data


def setup_logging(log_dir: Path) -> Path:
    """Configure logging and return the log file path."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path(log_dir) / f"generate_data_yaml_{timestamp}.log"
    logging.basicConfig(
        filename=log_path,
        filemode="w",
        level=logging.INFO,
        format='[%(levelname)s] %(message)s',
    )
    return log_path


def run(config_path: str) -> None:
    """Load config and generate a data.yaml file."""
    with open(config_path, "r") as f:
        cfg = json.load(f)

    data_dir = Path(os.getenv("DATA_DIR", "."))
    log_path = setup_logging(data_dir / "logs" / "data_yaml")
    print(f"[INFO] Log written to {log_path}\n")
    generate_data_yaml(cfg)


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m backend.generate_data_yaml <config.json>")
        sys.exit(1)
    run(argv[0])


if __name__ == "__main__":
    main()
