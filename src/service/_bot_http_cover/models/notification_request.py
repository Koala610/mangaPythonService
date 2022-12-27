from pydantic import BaseModel

class NotificationRequest(BaseModel):
    access_token: str
    message: str