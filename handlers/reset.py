from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text

import database.like
from client import bot
from tools import send_menu

dp = Dispatch()


@dp.message(Text("/reset"))
async def profile(m: Message):
    await m.answer("Ты правда хочешь сбросить свой профиль? Напиши: «Да» или «Нет»")
    m, _ = await bot.dispatch.message.wait_for_message(
        m.chat.id, Text(["да", "нет"], ignore_case=True), default="Да / Нет"
    )
    if m.text.lower() == "нет":
        await m.answer("Сброс профиля отменен.")
        await send_menu(m.chat.id)
        return

    await database.like.delete_all(m.from_.id)
    await database.user.delete(m.from_.id)
    await m.answer("Я отключил твой профиль.")
