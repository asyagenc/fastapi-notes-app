from typing import Optional
from sqlmodel import SQLModel


class NoteCreate(SQLModel):
    text: str
    important: bool = False
    username: str


class NoteUpdate(SQLModel):
    text: Optional[str] = None
    important: Optional[bool] = None
    username: Optional[str] = None

class UserCreate(SQLModel):
    username: str