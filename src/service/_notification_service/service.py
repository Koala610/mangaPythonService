import fastapi

from src.service._notification_service.routers import base

app = fastapi.FastAPI()
app.include_router(router=base.router)