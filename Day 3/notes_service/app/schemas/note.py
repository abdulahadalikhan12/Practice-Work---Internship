from pydantic import BaseModel
from datetime import datetime


class NoteCreate(BaseModel):
    """Shape of the JSON body the client sends to create a note."""
    content: str


class NoteUpdate(BaseModel):
    """Shape of the JSON body the client sends to edit a note."""
    content: str


class NoteOut(BaseModel):
    """
    Shape of the JSON the server sends back for a note.

    We never let the client set `id` or `created_at` themselves --
    those are server-assigned. Keeping this separate from NoteCreate
    is what stops a client from doing something like
    POST /notes {"id": 9999, "content": "hi"} and messing with our data.
    """
    id: str
    content: str
    created_at: datetime
