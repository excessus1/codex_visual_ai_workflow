import subprocess
import os
import sys
import json
from .utils import emit_status


def build_rsync_command(local_path, gcs_path, *, dry_run: bool = False, delete_extras: bool = False):
    """Build the ``gsutil rsync`` command.

    Args:
        local_path: Source directory on the local filesystem.
        gcs_path: Destination path in Google Cloud Storage.
        dry_run: If ``True``, include ``-n`` to perform a trial run with no
            changes made.
        delete_extras: If ``True``, include ``-d`` so that files present in the
            destination but not in the source are deleted.

    Returns:
        List[str]: The full command ready to be passed to ``subprocess``.
    """

    cmd = ["gsutil", "-m", "rsync", "-r"]
    if dry_run:
        cmd.append("-n")
    if delete_extras:
        cmd.append("-d")
    cmd.extend([local_path, gcs_path])
    return cmd


def _env_bool(name: str, default: bool = False) -> bool:
    """Return environment variable ``name`` interpreted as a boolean."""

    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def upload(config):
    local_path = os.path.expanduser(config["local_path"])
    gcs_path = config["gcs_path"]
    dry_run = config.get("dry_run", _env_bool("UPLOAD_GCS_DRY_RUN"))
    delete_extras = config.get(
        "delete_extras", _env_bool("UPLOAD_GCS_DELETE_EXTRAS")
    )
    emit_status("start", action="upload_gcs", source=local_path, destination=gcs_path)

    cmd = build_rsync_command(
        local_path, gcs_path, dry_run=dry_run, delete_extras=delete_extras
    )
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
