import datetime

import telegrinder
import edgedb
import logging
import uuid
from envparse import env

env.read_envfile(".env")

api = telegrinder.API(token=telegrinder.Token.from_env(is_read=True))
bot = telegrinder.Telegrinder(api)
fmt = telegrinder.tools.HTMLFormatter
db = edgedb.create_async_client()
logger = logging.getLogger("bot")
wm = telegrinder.WaiterMachine()

STARTED = datetime.datetime.now()
SYSTEM_ADMINS = (env.str("SYSTEM_ADMINS") or "").split(",")

SECRET = str(uuid.uuid4())[:-12]
JWT_ALG = env.str("jwt_alghorithm", default="HS256")
WEBAPP_URL = env.str("webapp_url")

