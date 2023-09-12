from fastapi import APIRouter, Request, Response, HTTPException, status
from client import SECRET
from telegrinder.types import Update
from bot import bot
import msgspec


router = APIRouter(prefix="/bot")
TEAPOT = HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)


@router.post("/update")
async def update_handler(request: Request) -> Response:
    """Telegram webhook updates receiver"""

    # verifying request
    header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if not header or header != SECRET:
        raise TEAPOT

    update = msgspec.json.decode(await request.body(), type=Update)
    await bot.dispatch.feed(update, bot.api)
    return Response(status_code=200)
