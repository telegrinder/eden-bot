from telegrinder.bot.rules import FuncRule, ABCMessageRule
from telegrinder import Message

LIKE_RECEIVED = FuncRule(lambda cb, _: cb["callback_query"]["data"].startswith("like/"))
REPORT_RECEIVED = FuncRule(
    lambda cb, _: cb["callback_query"]["data"].startswith("report/")
)
SETTING_TOGGLE_RECEIVED = FuncRule(
    lambda cb, _: cb["callback_query"].get("data", "")
    in ("toggle_city", "toggle_safe_mode", "toggle_search_city")
)


class HasPhoto(ABCMessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.photo is not None
