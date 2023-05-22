import fastapi

from src.service._bot_http_cover.routers import base
from .routers import jwt, notifications, bookmarks, user, support 
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:8081",
]

app = fastapi.FastAPI(docs_url="/docs")
app.include_router(router=base.router)
app.include_router(router=jwt.router)
app.include_router(router=notifications.router)
app.include_router(router=bookmarks.router)
app.include_router(router=user.router)
app.include_router(router=support.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)