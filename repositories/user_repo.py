import uuid
from sqlmodel import Session, select

from models import User


def get_all_users(session: Session):
    return session.exec(select(User)).all()


def get_user_by_id(session: Session, user_id: uuid.UUID):
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str):
    return session.exec(
        select(User).where(User.username == username)
    ).first()


def create_user(session: Session, username: str):
    user = User(username=username)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()