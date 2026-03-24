import uuid
from sqlmodel import Session, select

from models import Note


class NoteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_notes(self):
        return self.session.exec(select(Note)).all()

    def get_note_by_id(self, note_id: uuid.UUID):
        return self.session.get(Note, note_id)

    def get_notes_by_user_id(self, user_id: uuid.UUID):
        statement = select(Note).where(Note.user_id == user_id)
        return self.session.exec(statement).all()

    def create_note(self, note: Note):
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def save_note(self, note: Note):
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def delete_note(self, note: Note):
        self.session.delete(note)
        self.session.commit()