import uuid

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models import Note
from schemas import NoteCreate, NoteUpdate
from services.note_service import (
    create_note,
    get_note,
    get_notes,
    remove_note,
    replace_note,
    update_note,
)

router = APIRouter(prefix="/notes")


@router.post("", response_model=Note)
def create_note_route(note: NoteCreate, session: Session = Depends(get_session)):
    return create_note(session, note)


@router.get("", response_model=list[Note])
def get_notes_route(session: Session = Depends(get_session)):
    return get_notes(session)


@router.get("/{note_id}", response_model=Note)
def get_note_route(note_id: uuid.UUID, session: Session = Depends(get_session)):
    return get_note(session, note_id)


@router.put("/{note_id}", response_model=Note)
def replace_note_route(
    note_id: uuid.UUID,
    note: NoteCreate,
    session: Session = Depends(get_session)
):
    return replace_note(session, note_id, note)


@router.patch("/{note_id}", response_model=Note)
def update_note_route(
    note_id: uuid.UUID,
    note: NoteUpdate,
    session: Session = Depends(get_session)
):
    return update_note(session, note_id, note)


@router.delete("/{note_id}")
def delete_note_route(note_id: uuid.UUID, session: Session = Depends(get_session)):
    return remove_note(session, note_id)