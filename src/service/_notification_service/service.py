import fastapi
import src.service._notification_service.routers.base as base


app = fastapi.FastAPI()
app.include_router(router=base.router)