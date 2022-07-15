import typing
import datetime
import collections

from client import db, logger

GET_ADMIN = open("database/queries/get_admin.edgeql").read()
NEW_ADMIN = open("database/queries/new_admin.edgeql").read()
DEMOTE = open("database/queries/delete_admin.edgeql").read()
STATS = open("database/queries/get_stats.edgeql").read()


class Admin:
    """
    Fake type hint for user
    """

    telegram_id: str
    promoted_by: str
    promoted_at: datetime.datetime


async def get(telegram_id: int) -> typing.Optional[Admin]:
    admins = await db.query(GET_ADMIN, telegram_id=str(telegram_id))
    if not admins:
        return None
    return admins[0]


async def promote(telegram_id: int, promoter_id: int) -> typing.Optional[Admin]:
    promoter = await db.query(GET_ADMIN, telegram_id=str(promoter_id))
    if not promoter:
        return None
    logger.info(f"{promoter_id} promoting {telegram_id}")
    return (
        await db.query(
            NEW_ADMIN,
            telegram_id=str(telegram_id),
            promoted_by=str(promoter_id),
            promoted_at=datetime.datetime.now(),
        )
    )[0]


async def demote(telegram_id: int, demoter_id: int) -> typing.Optional[Admin]:
    demoter = await db.query(GET_ADMIN, telegram_id=str(demoter_id))
    if not demoter:
        return None
    demoted = await db.query(GET_ADMIN, telegram_id=str(telegram_id))
    if not demoted or demoted.promoted_by != str(demoter_id):
        return None
    await db.query(DEMOTE, telegram_id=str(telegram_id))


Stats = collections.namedtuple(
    "Stats", ["user_count", "boys_count", "like_count", "picture_count"]
)


async def get_stats() -> Stats:
    stats = await db.query(STATS)
    return Stats(*stats)
