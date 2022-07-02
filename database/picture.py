import typing

from client import db

DELETE = open("database/queries/delete_user_pictures.edgeql").read()
NEW = open("database/queries/new_picture.edgeql").read()
GET = open("database/queries/get_profile_picture.edgeql").read()
INSERT_MANY = open("database/queries/insert_many_pictures.edgeql").read()


class Picture:
    """
    Fake type hint for picture
    """

    by_tg_id: str
    file_id: str
    moderated: bool


async def delete_by_user(telegram_id: int):
    await db.query(DELETE, telegram_id=str(telegram_id))


async def new(telegram_id: int, file_id: str):
    await db.query(NEW, telegram_id=str(telegram_id), file_id=file_id)


async def get_profile_pictures(telegram_id: int) -> typing.List[Picture]:
    return await db.query(GET, telegram_id=str(telegram_id))


async def insert_many(telegram_id: int, file_ids: typing.List[str]):
    await db.query(INSERT_MANY, telegram_id=str(telegram_id), ids=file_ids)
