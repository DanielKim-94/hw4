from datetime import datetime, timezone
import json
import re
from pathlib import Path
from threading import Lock
from typing import Any

AUDIT_PATH = Path(__file__).resolve().parents[1] / "output" / "audit_trail.json"
_lock = Lock()

def _safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _safe(v) for k, v in value.items() if str(k).lower() not in {"password", "password_hash", "token", "api_key", "email"}}
    if isinstance(value, (list, tuple)):
        return [_safe(item) for item in value[:8]]
    text = str(value)
    text = re.sub(r"[\w.+-]+@[\w.-]+", "[redacted-email]", text)
    return text[:300]

def audit_event(tool_name: str, arguments: Any, result: Any, end_reason: str) -> None:
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "tool_name": tool_name[:80], "arguments": _safe(arguments), "result": _safe(result), "end_reason": end_reason[:160]}
    with _lock:
        AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            history = json.loads(AUDIT_PATH.read_text(encoding="utf-8")) if AUDIT_PATH.exists() else []
            if not isinstance(history, list):
                history = []
        except (json.JSONDecodeError, OSError):
            history = []
        history.append(entry)
        AUDIT_PATH.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
