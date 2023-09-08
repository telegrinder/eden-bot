import asyncio
import logging
import typing
import os

import database.picture
import telegrinder
import edgedb

from client import bot, db as async_db_client
import aiofiles
import threading
import queue
import nude

client = telegrinder.client.AiohttpClient()
db_client = edgedb.create_client()

nude_queue = queue.Queue()
bad_pictures = queue.Queue()

logger = logging.getLogger("nsfw")


async def save_picture(picture: database.picture.Picture, as_path: str) -> bool:
    file_result = await bot.api.get_file(picture.file_id)
    if not file_result.is_ok:
        return False
    file = file_result.unwrap()
    content = await client.request_content(
        bot.api.API_URL + f"file/bot{bot.api.token}/" + file.file_path
    )
    async with aiofiles.open(as_path, "wb") as stream:
        await stream.write(content)
    return True


async def put_picture(picture: database.picture.Picture) -> bool:
    name = "pic_" + picture.file_id + ".jpg"
    if not await save_picture(picture, name):
        return False
    nude_queue.put((picture, nude.Nude(name)))
    return True


def queue_parser():
    while True:
        logger.info("Waiting for new pictures to parse...")
        item: typing.Tuple[database.picture.Picture, nude.Nude] = nude_queue.get()
        logger.info("Parsing picture " + item[0].file_id)
        nude_pic = item[1]
        nude_pic.parse()
        if nude_pic.result:
            logger.info("Picture {} is nudity".format(item[0].file_id))
            bad_pictures.put(item[0])
        os.remove("pic_" + item[0].file_id + ".jpg")


def queue_deleter(loop: asyncio.AbstractEventLoop):
    while True:
        logger.info("Waiting for new bad pictures to delete...")
        item: database.picture.Picture = bad_pictures.get()
        logger.info("Deleting picture " + item.file_id)
        db_client.query("delete Picture filter .file_id = <str>$f", f=item.file_id)
        loop.create_task(
            bot.api.send_message(
                item.by_tg_id,
                text="🔞 В одной из твоих фотографий было обнаружено NSFW, поэтому она была удалена из профиля",
            )
        )


async def worker_put():
    while True:
        pictures = await async_db_client.query(
            "select Picture {file_id, by_tg_id, moderated} filter .moderated = false"
        )
        logger.info("Putting pictures")
        if pictures:
            await asyncio.gather(*(put_picture(pic) for pic in pictures))
            await async_db_client.query(
                "update Picture {file_id} filter contains(<array<str>>$ids, .file_id) set {moderated := true}",
                ids=[pic.file_id for pic in pictures],
            )
        logger.info("Pictures put")
        await asyncio.sleep(60)


def run_nude_detection_workers(loop: asyncio.AbstractEventLoop):
    logger.info("Running NSFW detection")
    loop.create_task(worker_put())
    threading.Thread(target=queue_parser).start()
    threading.Thread(target=queue_deleter, args=(loop,)).start()


def test_worker(path: str):
    return nude.Nude(path).parse().result
