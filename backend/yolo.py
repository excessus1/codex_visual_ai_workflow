import os
import sys
import json
import subprocess
from ultralytics import YOLO
from .utils import emit_status


def run_prediction(cfg):
    model_path = cfg['model']
    source = cfg['source']
    output = cfg['output']
    conf = cfg.get('conf', 0.25)

    emit_status('start', action='predict', model=model_path, source=source)

    os.makedirs(output, exist_ok=True)
    project = os.path.dirname(output)
    name = os.path.basename(output)

    model = YOLO(model_path)
    results = model.predict(
        source=source,
        save=True,
        save_txt=True,
        conf=conf,
        project=project,
        name=name,
        device=0,
        stream=True,
    )

    for r in results:
        emit_status('prediction', file=getattr(r, 'path', ''), detections=len(getattr(r, 'boxes', [])))

    if cfg.get('convert_to_ls'):
        emit_status('conversion_start')
        try:
            from .convert_yolo_to_ls import convert_yolo_to_ls
            convert_yolo_to_ls(cfg['convert_to_ls'])
            emit_status('conversion_complete')
        except Exception as e:
            emit_status('conversion_error', error=str(e))

    emit_status('complete', action='predict')


def run_training(cfg):
    model_path = cfg['model']
    data_yaml = cfg['data']
    output = cfg['output']
    epochs = cfg.get('epochs', 100)
    batch = cfg.get('batch', 16)
    imgsz = cfg.get('imgsz', 640)

    emit_status('start', action='train', model=model_path, data=data_yaml)

    os.makedirs(output, exist_ok=True)
    project = os.path.dirname(output)
    name = os.path.basename(output)

    model = YOLO(model_path)
    model.train(data=data_yaml, epochs=epochs, batch=batch, imgsz=imgsz, project=project, name=name, save=True, plots=True)

    emit_status('complete', action='train')


def run(config_path: str, mode_override: str | None = None) -> None:
    with open(config_path, "r") as f:
        cfg = json.load(f)
    if mode_override:
        cfg["mode"] = mode_override
    mode = cfg.get("mode")
    if mode == "predict":
        run_prediction(cfg)
    elif mode == "train":
        run_training(cfg)
    else:
        raise ValueError("'mode' must be either 'predict' or 'train'")


def main(argv: list[str] | None = None, mode_override: str | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m backend.yolo <config.json>")
        sys.exit(1)
    run(argv[0], mode_override=mode_override)


if __name__ == "__main__":
    main()
