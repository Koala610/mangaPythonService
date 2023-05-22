import fastapi
from fastapi import Header
from typing import Annotated
from src.service.bot import answer_message
from ..entity.message import MessageRequest
from ..services.admin_service import check_if_user_admin

router = fastapi.APIRouter()
@check_if_user_admin
@router.post("/message/answer")
async def answer_user_message(message: MessageRequest, authorization: Annotated[str or None, Header()] = Header(title="Authorization")):
    await answer_message(message_id=message.message_id, response=message.response, support_id=message.support_id)
    return {"status": "ok"}