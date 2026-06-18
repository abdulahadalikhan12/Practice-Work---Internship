from fastapi import APIRouter, HTTPException, Depends

from app.schemas.note import NoteCreate, NoteUpdate, NoteOut
from app.services.notes_service import NotesService
from app.core.config import settings

router = APIRouter(prefix="/notes", tags=["notes"])


def get_notes_service() -> NotesService:
    """
    A FastAPI "dependency". Instead of every route doing
    `service = NotesService(settings.NOTES_FILE_PATH)` itself, each route
    just declares `service: NotesService = Depends(get_notes_service)`
    and FastAPI calls this function for you and hands over the result.

    Right now this looks like overkill for one settings value, but it's
    the standard pattern -- it's what lets you swap in a fake/mock service
    during testing without touching route code at all.
    """
    return NotesService(settings.NOTES_FILE_PATH)


@router.get("/", response_model=list[NoteOut])
def list_notes(service: NotesService = Depends(get_notes_service)):
    return service.get_all()


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: str, service: NotesService = Depends(get_notes_service)):
    note = service.get_one(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/", response_model=NoteOut, status_code=201)
def create_note(payload: NoteCreate, service: NotesService = Depends(get_notes_service)):
    return service.create(payload.content)


@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: str, payload: NoteUpdate, service: NotesService = Depends(get_notes_service)):
    note = service.update(note_id, payload.content)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: str, service: NotesService = Depends(get_notes_service)):
    deleted = service.delete(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
