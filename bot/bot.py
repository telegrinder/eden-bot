from client import bot
from bot.handlers import dps
from bot.middlewares import (
    RegisterMiddleware,
    CheckLikesMiddleware,
    LastActiveMiddleware,
    AccessMiddleware,
)

import logging
from telegrinder.modules import logger

logger.setLevel(logging.DEBUG)

for dp in dps:
    bot.dispatch.message.handlers.extend(dp.message.handlers)
    bot.dispatch.default_handlers.extend(dp.default_handlers)
    bot.dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.dispatch.message.middlewares.extend(
    [
        AccessMiddleware(),
        RegisterMiddleware(),
        CheckLikesMiddleware(),
        LastActiveMiddleware(),
    ]
)
