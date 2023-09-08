from telegrinder import Dispatch, CallbackQuery

import database.like
from bot.tools.send import send_profile
from client import logger, fmt
from bot.rules import LIKE_RECEIVED
from telegrinder.tools.formatting import Mention

dp = Dispatch()


@dp.callback_query(LIKE_RECEIVED)
async def like(cb: CallbackQuery):
    uid = cb.data.replace("like/", "", 1)
    to_like = await database.user.get_by_uid(uid)

    if not to_like:
        await cb.answer("К сожалению эта анкета куда-то потерялась")
        return

    like_exists = await database.like.get_direct(
        cb.from_.id, int(to_like[0].telegram_id)
    )

    if like_exists:
        await cb.answer("Ты уже ставил лайк на эту анкету.")
        return

    mutual_like_exists = await database.like.get_direct(
        int(to_like[0].telegram_id), cb.from_.id
    )

    mutual = False

    if mutual_like_exists:
        logger.info("Mutual like {} to {}".format(cb.from_.id, to_like[0].telegram_id))
        await cb.answer("Лайк поставлен! У вас взаимная симпатия!")
        mutual = True
    else:
        logger.info("{} liked {}".format(cb.from_.id, to_like[0].telegram_id))
        await database.like.new(cb.from_.id, int(to_like[0].telegram_id))
        await cb.answer("Лайк поставлен!")

    replied_msg_id = cb.message.reply_to_message.message_id
    await cb.ctx_api.delete_message(cb.message.chat.id, cb.message.message_id)
    await cb.ctx_api.edit_message_caption(
        cb.message.chat.id,
        replied_msg_id,
        caption=f"[❤️] {cb.message.reply_to_message.caption}",
    )

    if mutual:
        user = (await database.user.get_full(telegram_id=cb.from_.id))[0]

        await cb.ctx_api.send_message(
            chat_id=cb.from_.id,
            text=fmt("Взаимный интерес! Начинай общаться {:bold}").format(
                Mention("👉 " + to_like[0].name, to_like[0].telegram_id)
            ),
            parse_mode=fmt.PARSE_MODE,
        )

        msg_2 = fmt(
            "Есть взаимный интерес! Начинай общаться {:bold}"
            + ("" if not cb.from_.username else f" / @{cb.from_.username}")
        ).format(
            Mention("👉 " + user.name, user.telegram_id),
        )

        await cb.ctx_api.send_message(
            chat_id=to_like[0].telegram_id,
            text=msg_2,
            reply_to_message_id=await send_profile(
                int(to_like[0].telegram_id), cb.from_.id
            ),
            parse_mode=fmt.PARSE_MODE,
        )
