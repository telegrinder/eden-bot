from telegrinder.bot.rules import FuncRule

LIKE_RECEIVED = FuncRule(lambda cb, _: cb["callback_query"]["data"].startswith("like/"))
REPORT_RECEIVED = FuncRule(
    lambda cb, _: cb["callback_query"]["data"].startswith("report/")
)
SETTING_TOGGLE_RECEIVED = FuncRule(
    lambda cb, _: cb["callback_query"].get("data", "")
    in ("toggle_city", "toggle_safe_mode", "toggle_search_city")
)
