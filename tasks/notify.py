import asyncio
import random
import typing

import client
import database

HOUR = 60 * 60
emojis = "🐊🦋✨"


async def notify_work(users: typing.List[database.user.User]):
    for user in users:
        await client.api.send_message(
            user.telegram_id,
            text=random.choice(emojis)
            + " Ты кому-то понравился, используй команду /requests, "
            "чтобы посмотреть профили этих людей",
        )


async def notify_task():
    await asyncio.sleep(60 * 15)
    while True:
        unseen = await database.like.unseen_smart()
        await notify_work(unseen)
        await asyncio.sleep(HOUR)
