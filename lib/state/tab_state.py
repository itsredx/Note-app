from typing import List, Optional
from lib.backend.models import Note
from lib.utils.shared_prefernce import PythraPreferences
from lib.backend.repository import NoteRepository

_PREF_PREFIX = "tab_state_"


class _TabState:
    def __init__(self):
        self.open_tabs: List[Note] = []
        self.active_tab_id: Optional[str] = None
        self._prefs = PythraPreferences()
        self._restore()

    def _restore(self):
        ids = self._prefs.get(f"{_PREF_PREFIX}ids", [])
        active = self._prefs.get(f"{_PREF_PREFIX}active", None)
        if ids:
            repo = NoteRepository()
            for nid in ids:
                note = repo.get_note(nid)
                if note:
                    self.open_tabs.append(note)
            if active and any(t.id == active for t in self.open_tabs):
                self.active_tab_id = active
            elif self.open_tabs:
                self.active_tab_id = self.open_tabs[-1].id

    def _persist(self):
        self._prefs.set(f"{_PREF_PREFIX}ids", [t.id for t in self.open_tabs])
        self._prefs.set(f"{_PREF_PREFIX}active", self.active_tab_id)

    def add_tab(self, note: Note):
        for existing in self.open_tabs:
            if existing.id == note.id:
                self.active_tab_id = note.id
                self._persist()
                return
        self.open_tabs.append(note)
        self.active_tab_id = note.id
        self._persist()

    def remove_tab(self, note_id: str):
        self.open_tabs = [t for t in self.open_tabs if t.id != note_id]
        if self.active_tab_id == note_id:
            if self.open_tabs:
                self.active_tab_id = self.open_tabs[-1].id
            else:
                self.active_tab_id = None
        self._persist()

    def set_active(self, note_id: str):
        self.active_tab_id = note_id
        self._persist()


tab_state = _TabState()
