import uuid

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models import Note, User
from schemas import UserCreate
from services.user_service import (
    create_user,
    get_user,
    get_user_notes_by_username,
    get_users,
    remove_user,
)

router = APIRouter(prefix="/users")


@router.post("", response_model=User)
def create_user_route(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(session, user)


@router.get("", response_model=list[User])
def get_users_route(session: Session = Depends(get_session)):
    return get_users(session)


@router.get("/{user_id}", response_model=User)
def get_user_route(user_id: uuid.UUID, session: Session = Depends(get_session)):
    return get_user(session, user_id)


@router.delete("/{user_id}")
def delete_user_route(user_id: uuid.UUID, session: Session = Depends(get_session)):
    return remove_user(session, user_id)


@router.get("/{username}/notes", response_model=list[Note])
def get_notes_by_username_route(username: str, session: Session = Depends(get_session)):
    return get_user_notes_by_username(session, username)