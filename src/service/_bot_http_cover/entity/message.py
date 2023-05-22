from pydantic import BaseModel
from typing import Optional

class MessageRequest(BaseModel):
    message_id: Optional[int]
    support_id: Optional[int]
    response: Optional[str]