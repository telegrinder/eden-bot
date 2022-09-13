import datetime

import telegrinder
import edgedb
import logging
from envparse import env

env.read_envfile(".env")

api = telegrinder.API(token=telegrinder.Token.from_env(is_read=True))
bot = telegrinder.Telegrinder(api)
fmt = telegrinder.tools.MarkdownFormatter
db = edgedb.create_async_client()
logger = logging.getLogger("bot")

STARTED = datetime.datetime.now()
SYSTEM_ADMINS = (env.str("SYSTEM_ADMINS") or "").split(",")
