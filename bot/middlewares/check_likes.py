import typing
from telegrinder import ABCMiddleware, Message
from client import logger
import database


class CheckLikesMiddleware(ABCMiddleware):
    async def post(self, m: Message, responses: typing.List[typing.Any], ctx: dict):
        likes = await database.like.get_unseen(m.chat.id)

        if likes:
            logger.info(f"Likes sent to {m.chat.first_name} ({m.chat.id})")
            await m.answer(
                f"Ты понравился {len(likes)} людям. Чтобы показать их, напиши /requests"
                if len(likes) > 1
                else "Ты понравился 1 человеку. Чтобы показать его, напиши /requests"
            )
