import config
from .routers import base

app = config.FastAPI()
app.include_router(router=base.router)