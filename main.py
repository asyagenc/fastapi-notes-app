import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Note, User
from schemas import NoteCreate, NoteUpdate, UserCreate
from exception_handlers import register_exception_handlers, error_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)


@app.get("/")
def health():
    return {"success": True, "status": "ok"}

@app.post("/users", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(User).where(User.username == user.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail=error_response("Username already exists.", "USERNAME_TAKEN")
        )

    new_user = User(username=user.username)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.get("/users", response_model=list[User])
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: uuid.UUID, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=error_response("User not found.", "USER_NOT_FOUND")
        )
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: uuid.UUID, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=error_response("User not found.", "USER_NOT_FOUND")
        )

    username = user.username
    session.delete(user)
    session.commit()

    return {
        "success": True,
        "message": f"User '{username}' deleted successfully"
    }

@app.get("/users/{username}/notes", response_model=list[Note])
def get_notes_by_username(username: str, session: Session = Depends(get_session)):
    user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=error_response("User not found.", "USER_NOT_FOUND")
        )

    return session.exec(
        select(Note).where(Note.user_id == user.id)
    ).all()


@app.post("/notes", response_model=Note)
def create_note(note: NoteCreate, session: Session = Depends(get_session)):
    user = session.exec(
        select(User).where(User.username == note.username)
    ).first()

    if not user:
        user = User(username=note.username)
        session.add(user)
        session.commit()
        session.refresh(user)

    db_note = Note(
        text=note.text,
        important=note.important,
        user_id=user.id
    )
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@app.get("/notes", response_model=list[Note])
def get_notes(session: Session = Depends(get_session)):
    return session.exec(select(Note)).all()


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: uuid.UUID, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=404,
            detail=error_response("Note not found.", "NOTE_NOT_FOUND")
        )
    return note


@app.put("/notes/{note_id}", response_model=Note)
def replace_note(note_id: uuid.UUID, note: NoteCreate, session: Session = Depends(get_session)):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(
            status_code=404,
            detail=error_response("Note not found.", "NOTE_NOT_FOUND")
        )

    user = session.exec(
        select(User).where(User.username == note.username)
    ).first()

    if not user:
        user = User(username=note.username)
        session.add(user)
        session.commit()
        session.refresh(user)

    db_note.text = note.text
    db_note.important = note.important
    db_note.user_id = user.id

    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@app.patch("/notes/{note_id}", response_model=Note)
def update_note(note_id: uuid.UUID, note: NoteUpdate, session: Session = Depends(get_session)):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(
            status_code=404,
            detail=error_response("Note not found.", "NOTE_NOT_FOUND")
        )

    if note.text is None and note.important is None and note.username is None:
        raise HTTPException(
            status_code=400,
            detail=error_response(
                "At least one field must be provided for update.",
                "EMPTY_UPDATE"
            )
        )

    if note.username is not None:
        user = session.exec(
            select(User).where(User.username == note.username)
        ).first()

        if not user:
            user = User(username=note.username)
            session.add(user)
            session.commit()
            session.refresh(user)

        db_note.user_id = user.id

    if note.text is not None:
        db_note.text = note.text
    if note.important is not None:
        db_note.important = note.important

    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@app.delete("/notes/{note_id}")
def delete_note(note_id: uuid.UUID, session: Session = Depends(get_session)):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(
            status_code=404,
            detail=error_response("Note not found.", "NOTE_NOT_FOUND")
        )

    session.delete(db_note)
    session.commit()

    return {
        "success": True,
        "message": f"Note with id {note_id} deleted successfully"
    }