from fastapi import FastAPI
from . import routes
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

app.include_router(routes.router)
