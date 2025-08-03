import json
import sys
from typing import Any


def emit_status(event: str, **data: Any) -> None:
    """Emit a JSON status message to stdout."""
    payload = {"event": event, **data}
    print(json.dumps(payload))
    sys.stdout.flush()
