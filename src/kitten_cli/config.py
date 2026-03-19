import os
from pathlib import Path

_xdg = os.environ.get("XDG_CACHE_HOME", "")
CACHE_BASE = Path(_xdg) if _xdg else Path.home() / ".cache"
MODELS_DIR = CACHE_BASE / "kitten-cli" / "models"

MODEL_REGISTRY = {
    "mini":      "KittenML/kitten-tts-mini-0.8",
    "micro":     "KittenML/kitten-tts-micro-0.8",
    "nano":      "KittenML/kitten-tts-nano-0.8",
    "nano-int8": "KittenML/kitten-tts-nano-0.8-int8",
}

# Priority order: best model first
_MODEL_PRIORITY = ["mini", "micro", "nano", "nano-int8"]


def _best_installed_model() -> str:
    for alias in _MODEL_PRIORITY:
        model_dir = MODELS_DIR / alias
        if model_dir.exists() and any(model_dir.iterdir()):
            return alias
    return _MODEL_PRIORITY[-1]


DEFAULT_MODEL = _best_installed_model()
DEFAULT_VOICE = "Jasper"
DEFAULT_SPEED = 1.0
SAMPLE_RATE = 24000
