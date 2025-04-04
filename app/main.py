from fastapi import FastAPI
from . import routes, db_json


app = FastAPI()

db.load_db()
app.include_router(routes.router)
