import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from repositories.note_repo import NoteRepository
from repositories.user_repo import UserRepository
from services.note_service import NoteService
from schemas import NoteCreate, NoteUpdate
from models import Note

router = APIRouter()


def get_note_service(session: Session = Depends(get_session)) -> NoteService:
    note_repo = NoteRepository(session)
    user_repo = UserRepository(session)
    return NoteService(note_repo, user_repo)


@router.get("/notes", response_model=list[Note])
def get_notes(service: NoteService = Depends(get_note_service)):
    return service.get_all_notes()


@router.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: uuid.UUID, service: NoteService = Depends(get_note_service)):
    return service.get_note(note_id)


@router.post("/notes", response_model=Note)
def create_note(note: NoteCreate, service: NoteService = Depends(get_note_service)):
    return service.create_note(note)


@router.patch("/notes/{note_id}", response_model=Note)
def update_note(
    note_id: uuid.UUID,
    note: NoteUpdate,
    service: NoteService = Depends(get_note_service),
):
    return service.update_note(note_id, note)


@router.delete("/notes/{note_id}")
def delete_note(note_id: uuid.UUID, service: NoteService = Depends(get_note_service)):
    return service.delete_note(note_id)