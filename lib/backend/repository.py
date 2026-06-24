import os
import json
from pathlib import Path
from typing import List, Optional

from lib.backend.models import Note


NOTES_FILE = "notes.json"


def _get_data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.getenv("APPDATA"))
    elif os.name == "posix":
        if "darwin" in os.sys.platform:
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".config"
    else:
        base = Path.home()
    app_dir = base / "Note App"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


class NoteRepository:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or _get_data_dir()
        self.notes_path = self.data_dir / NOTES_FILE
        self._notes: List[Note] = []
        self._load()

    def _load(self):
        if not self.notes_path.exists():
            self._notes = []
            return
        try:
            raw = self.notes_path.read_text(encoding="utf-8")
            data = json.loads(raw)
            self._notes = [Note.from_dict(item) for item in data]
        except (json.JSONDecodeError, OSError):
            self._notes = []

    def _save(self):
        raw = json.dumps([n.to_dict() for n in self._notes], indent=2, ensure_ascii=False)
        self.notes_path.write_text(raw, encoding="utf-8")

    def reload(self):
        self._load()

    def list_notes(self) -> List[Note]:
        return list(self._notes)

    def get_note(self, note_id: str) -> Optional[Note]:
        for n in self._notes:
            if n.id == note_id:
                return n
        return None

    def create_note(self, title: str = "Untitled", content: str = "", color: str = "#4DD0E1") -> Note:
        note = Note(title=title, content=content, color=color)
        self._notes.insert(0, note)
        self._save()
        return note

    def update_note(self, note_id: str, title: Optional[str] = None, content: Optional[str] = None, color: Optional[str] = None) -> Optional[Note]:
        note = self.get_note(note_id)
        if note is None:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if color is not None:
            note.color = color
        from datetime import datetime, timezone
        note.updated_at = datetime.now(timezone.utc).isoformat()
        self._save()
        return note

    def delete_note(self, note_id: str) -> bool:
        for i, n in enumerate(self._notes):
            if n.id == note_id:
                del self._notes[i]
                self._save()
                return True
        return False
