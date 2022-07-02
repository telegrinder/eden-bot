import datetime

from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text, Markup

import database.admin
from client import STARTED
from logic import AdminRule

dp = Dispatch()


@dp.message(Text("/stats"), AdminRule())
async def stats(m: Message):
    await m.answer(
        f"Последний перезапуск: {datetime.datetime.strftime(STARTED, '%d.%m.%Y %H:%M')}"
    )


@dp.message(Markup("/promote <to_promote:int>"), AdminRule())
async def promote(m: Message, to_promote: int):
    result = await database.admin.promote(to_promote, m.from_.id)
    if not result:
        await m.reply("Что-то пошло не так")
        return
    await m.reply("Готово")


@dp.message(Markup("/demote <to_demote:int>"), AdminRule())
async def demote(m: Message, to_demote: int):
    result = await database.admin.demote(to_demote, m.from_.id)
    if not result:
        await m.reply("Что-то пошло не так")
        return
    await m.reply("Готово")
