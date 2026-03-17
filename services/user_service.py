import uuid

from fastapi import HTTPException
from sqlmodel import Session

from exception_handlers import error_response
from repositories.note_repo import get_notes_by_user_id
from repositories.user_repo import (
    create_user as repo_create_user,
    delete_user as repo_delete_user,
    get_all_users as repo_get_all_users,
    get_user_by_id as repo_get_user_by_id,
    get_user_by_username as repo_get_user_by_username,
)
from schemas import UserCreate


def create_user(session: Session, user_data: UserCreate):
    existing = repo_get_user_by_username(session, user_data.username)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=error_response("Username already exists.", "USERNAME_TAKEN")
        )

    return repo_create_user(session, user_data.username)


def get_users(session: Session):
    return repo_get_all_users(session)


def get_user(session: Session, user_id: uuid.UUID):
    user = repo_get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=error_response("User not found.", "USER_NOT_FOUND")
        )
    return user


def remove_user(session: Session, user_id: uuid.UUID):
    user = repo_get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=error_response("User not found.", "USER_NOT_FOUND")
        )

    username = user.username
    repo_delete_user(session, user)

    return {
        "success": True,
        "message": f"User '{username}' deleted successfully"
    }


def get_user_notes_by_username(session: Session, username: str):
    user = repo_get_user_by_username(session, username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=error_response("User not found.", "USER_NOT_FOUND")
        )

    return get_notes_by_user_id(session, user.id)