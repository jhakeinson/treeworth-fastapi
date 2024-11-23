from fastapi import FastAPI
from .routes import streets

app = FastAPI()
app.include_router(streets.router)
