from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text
from bot.tools.send import send_menu
from client import WEBAPP_URL

dp = Dispatch()


@dp.message(Text(["/start", "меню"], ignore_case=True))
async def start(m: Message):
    await send_menu(m.chat.id)


from telegrinder import InlineKeyboard, InlineButton

@dp.message(Text("/app"))
async def app_handler(m: Message):
    print("helo")
    (await m.answer(
        text="Application", 
        reply_markup=(
            InlineKeyboard()
            .add(
                InlineButton("App", web_app={"url": WEBAPP_URL + "/app/uni"})
            ).get_markup()
        )
    )).unwrap()
