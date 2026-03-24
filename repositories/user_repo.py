import uuid
from sqlmodel import Session, select

from models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_users(self):
        return self.session.exec(select(User)).all()

    def get_user_by_id(self, user_id: uuid.UUID):
        return self.session.get(User, user_id)

    def get_user_by_username(self, username: str):
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    def create_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()