import typing

from client import db, bot


SEARCH_UNI = open("database/queries/search_uni.edgeql").read()
SET_UNI = open("database/queries/set_uni.edgeql").read()


class Uni:
    id: str
    name: str
    city: int


UniLst = typing.List[Uni]


async def search(q: str | None) -> UniLst:
    if q is None:
        return await db.query("select Uni {id, name, city}")
    return await db.query(SEARCH_UNI, q=q)


async def set_uni(telegram_id: str, uni_id: str | None) -> None:
    if uni_id is None:
        await db.query("update User set {university := {}}")
        await bot.api.send_message(telegram_id, text="Настройки изменены: без вуза")
        return
    await bot.api.send_message(telegram_id, text="Настройки изменены: вуз был обновлен")
    await db.query(SET_UNI, telegram_id=telegram_id, uni_id=uni_id)
