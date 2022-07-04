from client import bot
from handlers import dps
from middlewares import RegisterMiddleware, CheckLikesMiddleware, LastActiveMiddleware
import logging
from telegrinder.modules import logger as logg
from client import logger

logg.setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO)

for dp in dps:
    bot.dispatch.message.handlers.extend(dp.message.handlers)
    bot.dispatch.default_handlers.extend(dp.default_handlers)
    bot.dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.dispatch.message.middlewares.extend([
    RegisterMiddleware(),
    CheckLikesMiddleware(),
    LastActiveMiddleware()
])
logger.info("Running.")
bot.run_forever()
