import os
import sys
import json
from ultralytics import YOLO
from .utils import emit_status, set_status_callback


def run_prediction(cfg, db=None, batch: int = 1):
    model_path = cfg['model']
    source = cfg['source']
    output = cfg['output']
    conf = cfg.get('conf', 0.25)

    emit_status('start', action='predict', model=model_path, source=source)

    job_id = None
    if db is not None:
        job_id = db.createPrediction({
            'model_name': model_path,
            'source_path': source,
            'output_path': output,
            'confidence_threshold': conf,
            'status': 'running',
        })

        processed = 0

        def _cb(event: str, data: dict) -> None:
            nonlocal processed
            if event == 'prediction':
                processed += 1
                db.updatePrediction(job_id, {'results_count': processed})
            elif event == 'complete':
                db.updatePrediction(job_id, {
                    'status': 'complete',
                    'results_count': processed,
                    'output_path': output,
                })

        set_status_callback(_cb)

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
        batch=batch,
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

    if db is not None:
        set_status_callback(None)


def run_training(cfg, db=None):
    model_path = cfg['model']
    data_yaml = cfg['data']
    output = cfg['output']
    epochs = cfg.get('epochs', 100)
    batch = cfg.get('batch', 16)
    imgsz = cfg.get('imgsz', 640)

    emit_status('start', action='train', model=model_path, data=data_yaml)

    job_id = None
    if db is not None:
        job_id = db.createTrainingSession({
            'model_name': model_path,
            'dataset_path': data_yaml,
            'epochs': epochs,
            'batch_size': batch,
            'status': 'running',
        })

        def _cb(event: str, data: dict) -> None:
            if event == 'complete':
                db.updateTrainingSession(job_id, {
                    'status': 'complete',
                    'metrics': json.dumps({}),
                })

        set_status_callback(_cb)

    os.makedirs(output, exist_ok=True)
    project = os.path.dirname(output)
    name = os.path.basename(output)

    model = YOLO(model_path)
    model.train(data=data_yaml, epochs=epochs, batch=batch, imgsz=imgsz, project=project, name=name, save=True, plots=True)

    emit_status('complete', action='train')

    if db is not None:
        set_status_callback(None)


def run(config_path: str, mode_override: str | None = None, db=None) -> None:
    with open(config_path, "r") as f:
        cfg = json.load(f)
    if mode_override:
        cfg["mode"] = mode_override
    mode = cfg.get("mode")
    if mode == "predict":
        run_prediction(cfg, db=db, batch=cfg.get('batch', 1))
    elif mode == "train":
        run_training(cfg, db=db)
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
