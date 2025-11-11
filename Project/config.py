import json
from pathlib import Path
from typing import Any, Optional

_config_path = Path(__file__).resolve().parent / "config.json"
_config: Optional[dict] = None

def _ensure_loaded() -> None:
    global _config
    if _config is not None:
        return
    if not _config_path.exists():
        raise FileNotFoundError(f"Config file not found: {_config_path}")
    with _config_path.open("r", encoding="utf-8") as f:
        _config = json.load(f)

def load(key: str) -> Any:
    """
    Return the value for `key` from config.json.

    - If the config file is missing this will raise FileNotFoundError unless
      a non-None `default` is provided (in which case the default is returned).
    - If the key is not present in the config, `default` is returned.
    """
    try:
        _ensure_loaded()
    except FileNotFoundError:
        raise
    return _config.get(key)
