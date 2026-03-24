import uuid
from fastapi import HTTPException

from models import Note, User
from schemas import NoteCreate, NoteUpdate
from exception_handlers import error_response
from repositories.note_repo import NoteRepository
from repositories.user_repo import UserRepository


class NoteService:
    def __init__(self, note_repo: NoteRepository, user_repo: UserRepository):
        self.note_repo = note_repo
        self.user_repo = user_repo

    def get_all_notes(self):
        return self.note_repo.get_all_notes()

    def get_note(self, note_id: uuid.UUID):
        note = self.note_repo.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=404,
                detail=error_response("Note not found", "NOTE_NOT_FOUND")
            )
        return note

    def get_or_create_user(self, username: str):
        user = self.user_repo.get_user_by_username(username)
        if not user:
            user = User(username=username)
            user = self.user_repo.create_user(user)
        return user

    def create_note(self, note_data: NoteCreate):
        user = self.get_or_create_user(note_data.username)

        note = Note(
            text=note_data.text,
            important=note_data.important,
            user_id=user.id
        )
        return self.note_repo.create_note(note)

    def update_note(self, note_id: uuid.UUID, note_data: NoteUpdate):
        note = self.note_repo.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=404,
                detail=error_response("Note not found", "NOTE_NOT_FOUND")
            )

        update_data = note_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail=error_response("No fields provided for update", "EMPTY_UPDATE")
            )

        if "username" in update_data:
            user = self.get_or_create_user(update_data["username"])
            note.user_id = user.id

        if "text" in update_data:
            note.text = update_data["text"]

        if "important" in update_data:
            note.important = update_data["important"]

        return self.note_repo.save_note(note)

    def delete_note(self, note_id: uuid.UUID):
        note = self.note_repo.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=404,
                detail=error_response("Note not found", "NOTE_NOT_FOUND")
            )

        self.note_repo.delete_note(note)
        return {"message": f"Note with id {note_id} deleted"}