from contextlib import asynccontextmanager
from fastapi import FastAPI
from .lib.db.database import db
from .routes import streets


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables")
    try:
        db.create_tables()
        db.populate_tables()
    except Exception as e:
        print(f"Error creating tables: {e}")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(streets.router)
