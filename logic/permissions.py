import database.admin
from client import SYSTEM_ADMINS
from telegrinder.bot.rules import ABCMessageRule
from telegrinder import Message


class AdminRule(ABCMessageRule):
    async def check(self, m: Message, ctx: dict) -> bool:
        return await is_admin(m.from_.id)


async def is_admin(telegram_id: int) -> bool:
    if str(telegram_id) in SYSTEM_ADMINS:
        return True
    return (await database.admin.get(telegram_id)) is not None
