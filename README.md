# codex_visual_ai_workflow

This project creates a workflow framework that helps prepare a Vision Inference model to perform in real-life, custom environments. 

The push it towards the newly created website, but simple CLI support should remain as well. 

The app is mainly a collection of scripts that fetch files, organize files, transform as desired, stage for training, run training, run predictions, view media, and evenually bypass the need for LabelStudio basic annotation. 

Integration with cloud services is supported for annotation, along side full local as developed.  -- Label Studio is heavily geared for Cloud annotation flow, which may not be preferrable by some.


## Environment Variables

Configuration relies on a few environment variables which can be set in a `.env` file at the project root.
The backend loads this file automatically using [`python-dotenv`](https://pypi.org/project/python-dotenv/).

| Variable      | Description                               | Default               |
|---------------|-------------------------------------------|-----------------------|
| `DATA_DIR`    | Base directory for datasets and logs       | `./data`              |
| `SCRIPTS_DIR` | Location of Python utility scripts         | `./backend`           |
| `DB_PATH`     | Path to the workflow SQLite database file  | `./data/workflow.db`  |

When these variables are not provided, the application will fall back to the defaults above which are relative to the repository root.


## Prediction Configuration

Prediction jobs are driven by JSON configuration files. In addition to the existing keys (`mode`, `model`, `source`, `output`, and optional `conf`), the backend now supports a `batch` key:

| Key     | Description                                                                 |
|---------|-----------------------------------------------------------------------------|
| `batch` | Number of images or video frames to process at once. Set `1` for per-image inference or increase to enable batched video processing. |

Including `"batch": 1` in a config file enforces per-image inference. Larger values process multiple frames simultaneously during prediction.


