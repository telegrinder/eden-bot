import typing
import datetime

from client import db

if typing.TYPE_CHECKING:
    from .picture import Picture

FULL_USER = open("database/queries/full_user.edgeql").read()
NEW = open("database/queries/new_user.edgeql").read()
ADD_CHECKED = open("database/queries/add_checked.edgeql").read()
ADD_REPORT = open("database/queries/add_report.edgeql").read()
BY_UID = open("database/queries/user_by_uid.edgeql").read()
DELETE = open("database/queries/delete_user.edgeql").read()
SET_CITY = open("database/queries/set_city.edgeql").read()
TOGGLE_SEARCH_CITY = open("database/queries/toggle_search_city.edgeql").read()
TOGGLE_SAFE_MODE = open("database/queries/toggle_safe_mode.edgeql").read()

_ = typing.Any


class User:
    """
    Fake type hint for user
    """

    id: str
    uid: str
    pictures: typing.Iterable["Picture"]
    telegram_id: str
    name: str
    age: int
    description: str
    created_at: datetime.datetime
    last_active: datetime.datetime
    display: bool
    interest: str
    gender: int
    checked: typing.List[str]
    safe_mode: bool
    city: int
    city_written_name: str
    search_city: bool
    reported: int

    def __getitem__(self, item) -> _:
        ...


UserResponse = typing.List[User]


async def get_full(telegram_id: int) -> UserResponse:
    return await db.query(FULL_USER, telegram_id=str(telegram_id))


async def get_by_uid(uid: str) -> UserResponse:
    return await db.query(BY_UID, uid=uid)


async def new(telegram_id: int, **fields) -> UserResponse:
    return await db.query(
        NEW, telegram_id=str(telegram_id), time_now=datetime.datetime.now(), **fields
    )


async def add_checked(telegram_id: int, seen_id: int) -> UserResponse:
    return await db.query(
        ADD_CHECKED, telegram_id=str(telegram_id), seen_id=str(seen_id)
    )


async def add_report(uid: str) -> UserResponse:
    return await db.query(ADD_REPORT, uid=uid)


async def delete(telegram_id: int) -> UserResponse:
    return await db.query(DELETE, telegram_id=str(telegram_id))


async def set_city(
    telegram_id: int, city_id: int, written_name: str = ""
) -> UserResponse:
    return await db.query(
        SET_CITY,
        telegram_id=str(telegram_id),
        city_id=city_id,
        written_name=written_name,
    )


async def toggle_search_city(telegram_id: int) -> UserResponse:
    return await db.query(TOGGLE_SEARCH_CITY, telegram_id=str(telegram_id))


async def toggle_safe_mode(telegram_id: int) -> UserResponse:
    return await db.query(TOGGLE_SAFE_MODE, telegram_id=str(telegram_id))
