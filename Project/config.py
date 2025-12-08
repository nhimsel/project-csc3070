import json
import sys
from pathlib import Path
from typing import Any, Optional

# Don't compute the config path at import time; when PyInstaller bundles the app
# with --onefile it extracts bundled data to a runtime temp folder referenced by
# `sys._MEIPASS`. Use that path when available, otherwise fall back to the
# source file directory. This makes the code work in normal and frozen builds.

# Default configuration values
DEFAULTS: dict[str, Any] = {
    "api_url": "http://127.0.0.1:5000/v1/chat/completions",
    "hide_on_fullscreen": False,
    "outfit": "default"
}

_config: Optional[dict] = None

def _get_config_path() -> Path:
    """Return the most appropriate config.json path.

    Preference order:
      1. Directory next to the running executable (`sys.executable`) — this
         is where a user-accessible `config.json` should live for bundled apps.
      2. The source file directory (`__file__`) — useful during development.
      3. PyInstaller unpack dir (`sys._MEIPASS`) — fallback when resources are
         bundled inside the package (useful for --onefile when you included
         a default config in the bundle).
    The function returns the first existing `config.json` it finds; if none
    exist, it returns the path next to the executable (where we expect the
    user to place it).
    """
    exe_dir = Path(sys.executable).resolve().parent
    script_dir = Path(__file__).resolve().parent
    meipass_dir = Path(getattr(sys, "_MEIPASS", "")) if getattr(sys, "_MEIPASS", None) else None

    candidates = [exe_dir, script_dir]
    if meipass_dir:
        candidates.append(meipass_dir)

    for d in candidates:
        cfg = d / "config.json"
        if cfg.exists():
            return cfg

    # If none exist, return the user-facing location next to the executable.
    return exe_dir / "config.json"

def _ensure_loaded() -> None:
    global _config
    if _config is not None:
        return
    cfg_path = _get_config_path()
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as f:
        _config = json.load(f)

def load(key: str, default: Any = None) -> Any:
    """
    Return the value for `key` from config.json, with fallback to DEFAULTS.

    - If the config file is missing, returns the value from DEFAULTS[key] if present,
      otherwise returns the provided `default` parameter (or None).
    - If the key is not present in the config, checks DEFAULTS[key] next, then
      falls back to the provided `default` parameter (or None).
    """
    try:
        _ensure_loaded()
    except FileNotFoundError:
        # Config file missing; use DEFAULTS or the provided default
        if key in DEFAULTS:
            return DEFAULTS[key]
        return default

    # Config file loaded; check it first, then DEFAULTS, then the provided default
    if key in _config:
        return _config[key]
    if key in DEFAULTS:
        return DEFAULTS[key]
    return default
