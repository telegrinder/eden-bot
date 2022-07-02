from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text
from tools import send_menu

dp = Dispatch()


@dp.message(Text(["/start", "меню"], ignore_case=True))
async def start(m: Message):
    await send_menu(m.chat.id)
