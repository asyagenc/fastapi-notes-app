import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    notes: List["Note"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Note(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    text: str
    important: bool = False
    user_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="user.id",
        ondelete="CASCADE"
    )
    user: Optional[User] = Relationship(back_populates="notes") 