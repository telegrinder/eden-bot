from client import api
from telegrinder.types import InputMediaPhoto
from client import logger
from keyboard.keyboard import KeyboardSet
import database


async def send_profile(chat_id: int, uid: int) -> int:
    logger.info("Sending {} profile to {}".format(uid, chat_id))
    users = await database.user.get_full(uid)

    if not users:
        await api.send_message("Произошла какая-то ошибка")
        return 0

    user = users[0]

    text = f"{user.name}, {user.age}"
    if user.city:
        text += f", {user.city_written_name}"

    if user.description:
        text += f" – {user.description}"

    mid = (
        await api.send_media_group(
            chat_id,
            [
                InputMediaPhoto(
                    type="photo", media=photo.file_id, caption=text if i == 0 else None
                )
                for i, photo in enumerate(user.pictures)
            ],
        )
    ).unwrap()

    return mid[0].message_id


async def send_menu(chat_id: int):
    await api.send_message(
        chat_id,
        "Воспользуйся кнопками меню, чтобы управлять мной.",
        reply_markup=KeyboardSet.KEYBOARD_MENU.get_markup(),
    )
