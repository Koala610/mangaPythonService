import fastapi
from .routers import base

app = fastapi.FastAPI()
app.include_router(router=base.router)