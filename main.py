from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db_and_tables
from exception_handlers import register_exception_handlers
from routes.notes import router as notes_router
from routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)

app.include_router(users_router, tags=["Users"])
app.include_router(notes_router, tags=["Notes"])


@app.get("/")
def health():
    return {"success": True, "status": "ok"}