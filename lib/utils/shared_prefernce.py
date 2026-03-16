import os
import json
from pathlib import Path
from typing import Any, Dict
from cryptography.fernet import Fernet

# from pythra import Config
from pythra.core import config

# config = Config("../../config.yaml")

APP_NAME = config.get("app_name", "Note App")
PREF_FILE = "prefs.enc"
KEY_FILE = "secret.key"


def get_appdata_path() -> Path:
    """Cross-platform AppData location."""
    if os.name == "nt":
        base = Path(os.getenv("APPDATA"))
    elif os.name == "posix":
        if "darwin" in os.sys.platform:
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".config"
    else:
        base = Path.home()

    app_dir = base / APP_NAME
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


class PythraPreferences:
    def __init__(self):
        self.app_dir = get_appdata_path()
        self.key_path = self.app_dir / KEY_FILE
        self.pref_path = self.app_dir / PREF_FILE

        self.cipher = Fernet(self._load_or_create_key())
        self._data: Dict[str, Any] = self._load()

    # ----------------------------
    # Key Handling
    # ----------------------------
    def _load_or_create_key(self) -> bytes:
        if self.key_path.exists():
            return self.key_path.read_bytes()

        key = Fernet.generate_key()
        self.key_path.write_bytes(key)
        return key

    # ----------------------------
    # Data Handling
    # ----------------------------
    def _load(self) -> Dict[str, Any]:
        if not self.pref_path.exists():
            return {}

        encrypted = self.pref_path.read_bytes()
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())

    def _save(self):
        raw = json.dumps(self._data).encode()
        encrypted = self.cipher.encrypt(raw)
        self.pref_path.write_bytes(encrypted)

    # ----------------------------
    # Public API
    # ----------------------------
    def set(self, key: str, value: Any):
        self._data[key] = value
        self._save()

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def delete(self, key: str):
        if key in self._data:
            del self._data[key]
            self._save()

    def clear(self):
        self._data.clear()
        self._save()
        
if __name__ == "__main__":
    prefs = PythraPreferences()

    prefs.set("theme", "dark")
    prefs.set("window_size", [800, 600])
    prefs.set("nested", {"a": 1, "b": True})

    print(prefs.get("window_size"))
