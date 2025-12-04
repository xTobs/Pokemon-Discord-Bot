
import os
from dotenv import load_dotenv

# Lädt die .env-Datei
load_dotenv()

def _to_int(name: str, default: int) -> int:
    """Hilfsfunktion: liest eine Umgebungsvariable als int, fallback auf default."""
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default

def load_config() -> dict:
    """Lädt alle relevanten Konfigurationswerte aus .env und gibt sie als Dictionary zurück."""
    return {
        "DISCORD_TOKEN": os.getenv("DISCORD_TOKEN", "").strip(),
        "TEXT_CHANNEL_ID": _to_int("TEXT_CHANNEL_ID", 0),
        "VOICE_CHANNEL_ID": _to_int("VOICE_CHANNEL_ID", 0),
        "SPAWN_MIN_SEC": _to_int("SPAWN_MIN_SEC", 180),
        "SPAWN_MAX_SEC": _to_int("SPAWN_MAX_SEC", 300),
        "USE_THREADS": os.getenv("USE_THREADS", "0") == "1",
        "DEBUG": os.getenv("DEBUG", "0") == "1",}
