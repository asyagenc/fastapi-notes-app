import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from repositories.note_repo import NoteRepository
from repositories.user_repo import UserRepository
from services.user_service import UserService
from models import User, Note

router = APIRouter()


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    user_repo = UserRepository(session)
    note_repo = NoteRepository(session)
    return UserService(user_repo, note_repo)


@router.get("/users", response_model=list[User])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: uuid.UUID, service: UserService = Depends(get_user_service)):
    return service.get_user(user_id)


@router.get("/users/{username}/notes", response_model=list[Note])
def get_user_notes(username: str, service: UserService = Depends(get_user_service)):
    return service.get_user_notes_by_username(username)