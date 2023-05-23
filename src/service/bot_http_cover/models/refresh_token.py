from pydantic import BaseModel
from typing import Optional

class TokenRequest(BaseModel):
    refresh_token: Optional[str]
    access_token: Optional[str]