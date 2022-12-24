import fastapi

from src.service._bot_http_cover.routers import base

app = fastapi.FastAPI()
app.include_router(router=base.router)