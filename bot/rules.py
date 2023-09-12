import database.admin
from client import SYSTEM_ADMINS
from telegrinder.bot.rules import MessageRule
from telegrinder import Message
from telegrinder.bot.rules import FuncRule


async def is_admin(telegram_id: int) -> bool:
    if str(telegram_id) in SYSTEM_ADMINS:
        return True
    return (await database.admin.get(telegram_id)) is not None


LIKE_RECEIVED = FuncRule(
    lambda cb, _: (cb.callback_query.data or "").startswith("like/")
)
REPORT_RECEIVED = FuncRule(
    lambda cb, _: (cb.callback_query.data or "").startswith("report/")
)
SETTING_TOGGLE_RECEIVED = FuncRule(
    lambda cb, _: (cb.callback_query.data or "")
    in ("toggle_city", "toggle_safe_mode", "toggle_search_city")
)


class HasPhoto(MessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.photo is not None


class AdminRule(MessageRule):
    async def check(self, m: Message, ctx: dict) -> bool:
        return await is_admin(m.from_.id)
