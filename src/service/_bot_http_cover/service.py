import fastapi

from src.service._bot_http_cover.routers import base
from .routers import jwt
from .routers import notifications

app = fastapi.FastAPI(docs_url="/docs")
app.include_router(router=base.router)
app.include_router(router=jwt.router)
app.include_router(router=notifications.router)