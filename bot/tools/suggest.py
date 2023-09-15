import typing
from database.user import User
from client import db
import random


genders = {"b": 0, "g": 1}


def build_query(user: User) -> typing.List[str]:
    q = []
    for c in user.interest:
        if c == "f" or genders.get(c) == user.gender:
            # homo interest or friend interest
            q.append(
                f"(select User filter <str>'{c}' in array_unpack(str_split(.interest, ''))\n"
                "and suggest_to.age > (.age - 3)\n"
                "and suggest_to.age < (.age + 3)\n"
                "and .telegram_id != suggest_to.telegram_id\n"
                "order by .last_active desc then .created_at)"
            )
        else:
            # hetero interest
            if user.gender == 0:
                q.append(
                    f"(select User\n"
                    f"filter .gender = {genders[c]}\n"
                    "and suggest_to.age > (.age - 5)\n"
                    "and suggest_to.age < (.age + 3)\n"
                    f"order by .last_active desc then .created_at)"
                )
            else:
                q.append(
                    f"(select User\n"
                    f"filter .gender = {genders[c]}\n"
                    "and suggest_to.age > (.age - 3)\n"
                    "and suggest_to.age < (.age + 6)\n"
                    f"order by .last_active desc then .created_at)"
                )
    return q


async def suggest(user: User) -> typing.List[User]:
    qs = build_query(user)
    q = (
        "with suggest_to := (select User { id, telegram_id, checked, university: {name} } filter .telegram_id = <str>$telegram_id), "
        "A := (select distinct " + " union ".join(qs) + ")\n"
        "select A {name, telegram_id} filter .telegram_id not in array_unpack(suggest_to.checked) and .display = true "
        "and .reported < 5"
    )
    if user.city and user.search_city:
        q += " and " + ".city = suggest_to.city"

    if user.university:
        q += " and .university = suggest_to.university"
    else:
        q += " and not exists .university"

    q += " order by .last_active desc limit 10"
    suggestions = list(await db.query(q, telegram_id=user.telegram_id))
    random.shuffle(suggestions)
    return suggestions
