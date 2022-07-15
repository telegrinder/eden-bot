import time
import typing
import datetime

from client import db

if typing.TYPE_CHECKING:
    from .user import User


GET_LIKE = open("database/queries/get_like.edgeql").read()
UNSEEN_LIKES = open("database/queries/unseen_likes.edgeql").read()
NEW = open("database/queries/new_like.edgeql").read()
SET_SEEN = open("database/queries/like_set_seen.edgeql").read()
DELETE = open("database/queries/delete_likes.edgeql").read()
UNSEEN_SM = open("database/queries/likes_smart.edgeql").read()

STOP_SHOWING = 60 * 60 * 3


class Like:
    """
    Fake type hint for like
    in queries named as `Like` (with grave accent)
    """

    from_user: "User"
    to_user: "User"
    seen: bool


async def get_direct(from_id: int, to_id: int) -> typing.List[Like]:
    return await db.query(GET_LIKE, from_id=str(from_id), to_id=str(to_id))


async def get_unseen(telegram_id: int) -> typing.List[Like]:
    return await db.query(UNSEEN_LIKES, telegram_id=str(telegram_id))


async def new(from_user_id: int, to_user_id: int):
    await db.query(NEW, from_user_id=str(from_user_id), to_user_id=str(to_user_id))


async def set_seen(telegram_id: int):
    await db.query(SET_SEEN, telegram_id=str(telegram_id))


async def delete_all(telegram_id: int):
    await db.query(DELETE, telegram_id=str(telegram_id))


async def unseen_smart() -> typing.List["User"]:
    return await db.query(
        UNSEEN_SM,
        min_online=datetime.datetime.fromtimestamp(time.time() - STOP_SHOWING),
    )
