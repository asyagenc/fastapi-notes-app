import uuid

from fastapi import HTTPException
from sqlmodel import Session

from exception_handlers import error_response
from repositories.note_repo import (
    create_note as repo_create_note,
    delete_note as repo_delete_note,
    get_all_notes as repo_get_all_notes,
    get_note_by_id as repo_get_note_by_id,
    save_note as repo_save_note,
)
from repositories.user_repo import (
    create_user as repo_create_user,
    get_user_by_username as repo_get_user_by_username,
)
from schemas import NoteCreate, NoteUpdate


def get_or_create_user(session: Session, username: str):
    user = repo_get_user_by_username(session, username)
    if not user:
        user = repo_create_user(session, username)
    return user


def create_note(session: Session, note_data: NoteCreate):
    user = get_or_create_user(session, note_data.username)

    return repo_create_note(
        session=session,
        text=note_data.text,
        important=note_data.important,
        user_id=user.id
    )


def get_notes(session: Session):
    return repo_get_all_notes(session)


def get_note(session: Session, note_id: uuid.UUID):
    note = repo_get_note_by_id(session, note_id)
    if not note:
        raise HTTPException(
            status_code=404,
            detail=error_response("Note not found.", "NOTE_NOT_FOUND")
        )
    return note


def replace_note(session: Session, note_id: uuid.UUID, note_data: NoteCreate):
    db_note = repo_get_note_by_id(session, note_id)
    if not db_note:
        raise HTTPException(
            status_code=404,
            detail=error_response("Note not found.", "NOTE_NOT_FOUND")
        )

    user = get_or_create_user(session, note_data.username)

    db_note.text = note_data.text
    db_note.important = note_data.important
    db_note.user_id = user.id

    return repo_save_note(session, db_note)


def update_note(session: Session, note_id: uuid.UUID, note_data: NoteUpdate):
    db_note = repo_get_note_by_id(session, note_id)
    if not db_note:
        raise HTTPException(
            status_code=404,
            detail=error_response("Note not found.", "NOTE_NOT_FOUND")
        )

    if note_data.text is None and note_data.important is None and note_data.username is None:
        raise HTTPException(
            status_code=400,
            detail=error_response(
                "At least one field must be provided for update.",
                "EMPTY_UPDATE"
            )
        )

    if note_data.username is not None:
        user = get_or_create_user(session, note_data.username)
        db_note.user_id = user.id

    if note_data.text is not None:
        db_note.text = note_data.text

    if note_data.important is not None:
        db_note.important = note_data.important

    return repo_save_note(session, db_note)


def remove_note(session: Session, note_id: uuid.UUID):
    db_note = repo_get_note_by_id(session, note_id)
    if not db_note:
        raise HTTPException(
            status_code=404,
            detail=error_response("Note not found.", "NOTE_NOT_FOUND")
        )

    repo_delete_note(session, db_note)

    return {
        "success": True,
        "message": f"Note with id {note_id} deleted successfully"
    }