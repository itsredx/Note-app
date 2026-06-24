from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime, timezone
import uuid


@dataclass
class Note:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    title: str = "Untitled"
    content: str = ""
    color: str = "#4DD0E1"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @staticmethod
    def from_dict(data: dict) -> "Note":
        return Note(
            id=data.get("id", uuid.uuid4().hex[:12]),
            title=data.get("title", "Untitled"),
            content=data.get("content", ""),
            color=data.get("color", "#4DD0E1"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat()),
        )

    def to_dict(self) -> dict:
        return asdict(self)
