import uuid
from fastapi import HTTPException

from models import User
from exception_handlers import error_response
from repositories.note_repo import NoteRepository
from repositories.user_repo import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository, note_repo: NoteRepository):
        self.user_repo = user_repo
        self.note_repo = note_repo

    def get_all_users(self):
        return self.user_repo.get_all_users()

    def get_user(self, user_id: uuid.UUID):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=error_response("User not found", "USER_NOT_FOUND")
            )
        return user

    def create_user(self, username: str):
        existing_user = self.user_repo.get_user_by_username(username)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail=error_response("Username already exists", "USERNAME_EXISTS")
            )

        user = User(username=username)
        return self.user_repo.create_user(user)

    def delete_user(self, user_id: uuid.UUID):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=error_response("User not found", "USER_NOT_FOUND")
            )

        self.user_repo.delete_user(user)
        return {"message": f"User with id {user_id} deleted"}

    def get_user_notes_by_username(self, username: str):
        user = self.user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=error_response("User not found", "USER_NOT_FOUND")
            )

        return self.note_repo.get_notes_by_user_id(user.id)