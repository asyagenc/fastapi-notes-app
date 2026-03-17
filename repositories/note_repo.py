import uuid
from sqlmodel import Session, select

from models import Note


def get_all_notes(session: Session):
    return session.exec(select(Note)).all()


def get_note_by_id(session: Session, note_id: uuid.UUID):
    return session.get(Note, note_id)


def get_notes_by_user_id(session: Session, user_id: uuid.UUID):
    return session.exec(
        select(Note).where(Note.user_id == user_id)
    ).all()


def create_note(session: Session, text: str, important: bool, user_id):
    note = Note(text=text, important=important, user_id=user_id)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def save_note(session: Session, note: Note):
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def delete_note(session: Session, note: Note):
    session.delete(note)
    session.commit()