import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from app.schemas.note import NoteOut


class NotesService:
    """
    All logic for storing notes inside a single JSON-array .txt file lives here.

    Why a class instead of plain functions? Mainly so we can hand the file
    path in once (via __init__) and reuse it across calls, and so FastAPI's
    Depends() has a clean object to construct and inject into routes -- see
    routers/notes.py. For this simple project a class is slightly more
    structure than strictly necessary, but it mirrors how a real "Service"
    layer would look if this grew (e.g. swapped for a database later).
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """If notes.txt doesn't exist yet, create it with an empty JSON array."""
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _read_all(self) -> List[dict]:
        """Read the whole file and parse it as a JSON array of note dicts."""
        raw = self.file_path.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        return json.loads(raw)

    def _write_all(self, notes: List[dict]) -> None:
        """Overwrite the file with the given list, pretty-printed for readability."""
        self.file_path.write_text(json.dumps(notes, indent=2, default=str), encoding="utf-8")

    # ---- Public CRUD methods used by the router ----

    def get_all(self) -> List[NoteOut]:
        return [NoteOut(**n) for n in self._read_all()]

    def get_one(self, note_id: str) -> Optional[NoteOut]:
        for n in self._read_all():
            if n["id"] == note_id:
                return NoteOut(**n)
        return None

    def create(self, content: str) -> NoteOut:
        notes = self._read_all()
        new_note = {
            "id": str(uuid.uuid4()),
            "content": content,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        notes.append(new_note)
        self._write_all(notes)
        return NoteOut(**new_note)

    def update(self, note_id: str, content: str) -> Optional[NoteOut]:
        notes = self._read_all()
        for n in notes:
            if n["id"] == note_id:
                n["content"] = content
                self._write_all(notes)
                return NoteOut(**n)
        return None  # caller (router) turns this into a 404

    def delete(self, note_id: str) -> bool:
        notes = self._read_all()
        filtered = [n for n in notes if n["id"] != note_id]
        if len(filtered) == len(notes):
            return False  # nothing was removed -> id didn't exist
        self._write_all(filtered)
        return True
