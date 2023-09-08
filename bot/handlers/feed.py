from telegrinder import Dispatch, Message, InlineKeyboard, InlineButton
from telegrinder.bot.rules import Text
from bot.tools.send import send_profile, send_menu
from bot.tools.suggest import suggest
from database.user import User, add_checked
from bot.keyboard.generators import KeyboardSet, no_kb

dp = Dispatch()


@dp.message(
    Text(["/feed", "смотреть анкеты", "смотреть профили", "дальше"], ignore_case=True)
)
async def feed(m: Message, user: User):
    suggestions = await suggest(user)
    if not suggestions:
        await m.answer("Пока мне больше нечего тебе показать", reply_markup=no_kb)
        await send_menu(m.chat.id)
    else:
        if m.text.lower() != "дальше":
            await m.answer(
                "Показываю анкеты", reply_markup=KeyboardSet.KEYBOARD_NEXT.get_markup()
            )
        suggestion = suggestions[0]
        mid = await send_profile(m.chat.id, int(suggestion.telegram_id))
        await add_checked(m.chat.id, int(suggestion.telegram_id))

        if mid:
            like_kb = (
                InlineKeyboard()
                .add(InlineButton("❤️", callback_data=f"like/{suggestion.id}"))
                .add(InlineButton("жалоба", callback_data=f"report/{suggestion.id}"))
                .get_markup()
            )
            await m.ctx_api.send_message(
                m.chat.id, text=" ㅤㅤㅤ", reply_markup=like_kb, reply_to_message_id=mid
            )
