import fastapi

from src.service._bot_http_cover.routers import base
from .routers import jwt

app = fastapi.FastAPI(docs_url="/docs")
app.include_router(router=base.router)
app.include_router(router=jwt.router)