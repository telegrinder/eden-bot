import database.admin
from client import SYSTEM_ADMINS
from telegrinder.bot.rules import ABCRule


class AdminRule(ABCRule):
    async def check(self, m: dict, ctx: dict) -> bool:
        return await is_admin(m["message"]["from_"]["id"])


async def is_admin(telegram_id: int) -> bool:
    if str(telegram_id) in SYSTEM_ADMINS:
        return True
    return (await database.admin.get(telegram_id)) is not None
