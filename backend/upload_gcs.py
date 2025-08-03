import subprocess
import os
import sys
import json
from .utils import emit_status

DRY_RUN = False
DELETE_EXTRAS = False


def build_rsync_command(local_path, gcs_path):
    cmd = ['gsutil', '-m', 'rsync', '-r']
    if DRY_RUN:
        cmd.append('-n')
    if DELETE_EXTRAS:
        cmd.append('-d')
    cmd.extend([local_path, gcs_path])
    return cmd


def upload(config):
    local_path = os.path.expanduser(config['local_path'])
    gcs_path = config['gcs_path']
    emit_status('start', action='upload_gcs', source=local_path, destination=gcs_path)

    cmd = build_rsync_command(local_path, gcs_path)
    try:
        subprocess.run(cmd, check=True)
        emit_status('complete', action='upload_gcs')
    except subprocess.CalledProcessError as e:
        emit_status('error', action='upload_gcs', message=str(e))


def run(config_path: str) -> None:
    with open(config_path, "r") as f:
        cfg = json.load(f)
    upload(cfg)


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m backend.upload_gcs <config.json>")
        sys.exit(1)
    run(argv[0])


if __name__ == "__main__":
    main()
