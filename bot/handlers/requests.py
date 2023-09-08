from telegrinder import Dispatch, Message, InlineKeyboard, InlineButton
from telegrinder.bot.rules import Text
from telegrinder.types import InputMediaPhoto

import database.like
from bot.tools.send import send_menu

dp = Dispatch()


@dp.message(Text(["/requests"]))
async def profile(m: Message):
    likes = await database.like.get_unseen(m.chat.id)

    if not likes:
        await m.answer("Пока новых лайков не было.")

    for i, like in enumerate(likes):
        like_kb = (
            InlineKeyboard()
            .add(InlineButton("❤️", callback_data=f"like/{like.from_user.id}"))
            .add(InlineButton("жалоба", callback_data=f"report/{like.from_user.id}"))
            .get_markup()
        )

        if i < len(likes) - 1:
            caption = f"С тобой хочет познакомится {like.from_user.name} и еще {len(likes) - i - 1} человек\n\n"
        else:
            caption = "С тобой хочет познакомится:\n\n"

        caption += f"{like.from_user.name}, {like.from_user.age}"
        if like.from_user.description:
            caption += f" – {like.from_user.description}"

        mid = (
            (
                await m.ctx_api.send_media_group(
                    m.chat.id,
                    media=[
                        InputMediaPhoto(
                            type="photo",
                            media=photo.file_id,
                            caption=caption if i == 0 else None,
                        )
                        for i, photo in enumerate(like.from_user.pictures)
                    ],
                )
            )
            .unwrap()[0]
            .message_id
        )

        await m.ctx_api.send_message(
            m.chat.id, text=" ㅤㅤㅤ", reply_markup=like_kb, reply_to_message_id=mid
        )

    await database.like.set_seen(m.chat.id)
    await send_menu(m.chat.id)
