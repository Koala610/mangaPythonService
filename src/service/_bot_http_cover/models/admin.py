from pydantic import BaseModel

class AdminInfo(BaseModel):
    id: int
    user_id: str