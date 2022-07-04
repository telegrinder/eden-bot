import typing
from telegrinder import ABCMiddleware, Message
import database
from client import logger
import time

MAX_NOT_UPDATED = 60


class LastActiveMiddleware(ABCMiddleware):
    async def post(self, m: Message, responses: typing.List[typing.Any], ctx: dict):
        assert "user" in ctx
        user = ctx["user"]
        # Last active timestamp will be updated
        # not more than once in MAX_NOT_UPDATED seconds
        if time.time() - user.last_active.timestamp() > MAX_NOT_UPDATED:
            logger.debug(f"Last active for {user.telegram_id} updated")
            await database.user.update_last_active(m.from_.id)
