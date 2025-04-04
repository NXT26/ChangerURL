from fastapi import FastAPI
from . import routes, db


app = FastAPI()

db.load_db()
app.include_router(routes.router)
