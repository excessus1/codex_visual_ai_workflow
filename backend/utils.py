import json
import sys
from typing import Any, Callable, Optional

_status_callback: Optional[Callable[[str, dict], None]] = None


def set_status_callback(cb: Optional[Callable[[str, dict], None]]) -> None:
    """Register a callback invoked whenever :func:`emit_status` is called."""
    global _status_callback
    _status_callback = cb


def emit_status(event: str, **data: Any) -> None:
    """Emit a JSON status message to stdout and invoke the status callback."""
    payload = {"event": event, **data}
    print(json.dumps(payload))
    sys.stdout.flush()
    if _status_callback is not None:
        _status_callback(event, data)
