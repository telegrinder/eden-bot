import dataclasses

from telegrinder import Dispatch, Message, InlineKeyboard, InlineButton, CallbackQuery
from telegrinder.bot.rules import Text, FuncRule
from telegrinder.types import InlineKeyboardMarkup

import database.picture
from database.user import User
from client import api, bot, db
from keyboard.set import no_kb, KeyboardSet
from tools import send_profile, send_menu
import typing

dp = Dispatch()


def get_profile_inline_menu(user: User):
    return (
        InlineKeyboard(resize_keyboard=True)
        .add(InlineButton("Редактировать", callback_data="profile/edit"))
        .add(
            InlineButton(
                "Скрыть" if user.display else "Открыть",
                callback_data="profile/toggle_hide",
            )
        )
        .get_markup()
    )


HIDDEN_PIN = "\n\n📍Сейчас твой профиль не выводится в поиске, чтобы он снова показывался там, нажми «Открыть»."


async def edit_name(chat_id: int):
    await api.send_message(
        chat_id,
        "Напиши мне твое новое имя",
        reply_markup=KeyboardSet.KEYBOARD_UNDO.get_markup(),
    )
    m, _ = await bot.dispatch.message.wait_for_message(chat_id)
    if not m.text or m.text.lower() == "отменить":
        return
    await db.query(
        "update User filter .telegram_id = <str>$telegram_id set {name := <str>$name}",
        telegram_id=str(chat_id),
        name=m.text,
    )
    await api.send_message(chat_id, "Имя изменено.", reply_markup=no_kb)


async def edit_age(chat_id: int):
    await api.send_message(
        chat_id,
        "Напиши твой возраст, например: 19",
        reply_markup=KeyboardSet.KEYBOARD_UNDO.get_markup(),
    )
    m, _ = await bot.dispatch.message.wait_for_message(
        chat_id,
        FuncRule(
            lambda msg, _: msg.text
            and (
                (msg.text.isdigit() and 15 <= int(msg.text) <= 100)
                or msg.text.lower() == "отменить"
            )
        ),
        default="Пожалуйста напиши возвраст числом, учти, что минимальный "
        "возраст 15 лет",
    )
    if m.text.lower() == "отменить":
        return
    age = int(m.text)
    await db.query(
        "update User filter .telegram_id = <str>$telegram_id set {age := <int16>$age}",
        telegram_id=str(chat_id),
        age=age,
    )
    await api.send_message(chat_id, "Возраст изменен.", reply_markup=no_kb)


async def edit_pictures(chat_id: int):
    await api.send_message(
        chat_id,
        "Пришли новую фотографию для своего профиля.",
        reply_markup=KeyboardSet.KEYBOARD_UNDO.get_markup(),
    )

    photos: typing.List[str] = []
    while len(photos) < 3:
        ph_m, _ = await bot.dispatch.message.wait_for_message(
            chat_id,
            FuncRule(
                lambda msg, _: (
                    msg.text
                    and (
                        (msg.text.lower() in ("это все", "это всё") and len(photos))
                        or msg.text.lower() == "отменить"
                    )
                )
                or msg.photo
            ),
            default="Пришли фотографию для твоего профиля",
        )
        if ph_m.text and ph_m.text.lower() in ("это все", "это всё", "отменить"):
            if ph_m.text.lower() == "отменить":
                return
            break
        photos.append(ph_m.photo[-1].file_id)
        if len(photos) < 3:
            await api.send_message(
                chat_id,
                "Добавил, пришли мне еще, если хочешь добавить "
                "еще фотографию в профиль, или напиши «это все».",
                reply_markup=KeyboardSet.KEYBOARD_THATS_ALL.get_markup(),
            )

    await database.picture.delete_by_user(chat_id)
    await database.picture.insert_many(chat_id, photos)

    await api.send_message(chat_id, "Фотографии успешно изменены.")


async def edit_description(chat_id: int):
    await api.send_message(
        chat_id,
        "Пришли мне новое описание для твоего профиля",
        reply_markup=KeyboardSet.KEYBOARD_UNDO_EMPTY.get_markup(),
    )
    m, _ = await bot.dispatch.message.wait_for_message(chat_id)
    if not m.text or m.text.lower() == "отменить":
        return
    description = m.text
    if description.lower() == "оставить пустым":
        description = ""
    await db.query(
        "update User filter .telegram_id = <str>$telegram_id set {description := <str>$description}",
        telegram_id=str(chat_id),
        description=description,
    )
    await api.send_message(chat_id, "Описание изменено.", reply_markup=no_kb)


async def edit_gender(chat_id: int):
    await api.send_message(
        chat_id,
        "Ты парень или девушка?",
        reply_markup=KeyboardSet.KEYBOARD_GENDER.get_markup(),
    )
    m, _ = await bot.dispatch.message.wait_for_message(
        chat_id,
        Text(["парень", "девушка", "отменить"], ignore_case=True),
        default="Выбери либо «парень», либо «девушка»",
    )

    if m.text.lower() == "отменить":
        return

    gender = 0 if m.text.lower() == "парень" else 1
    await db.query(
        "update User filter .telegram_id = <str>$telegram_id set {gender := <int16>$gender}",
        telegram_id=str(chat_id),
        gender=gender,
    )
    await api.send_message(chat_id, "Настройки пола изменены.", reply_markup=no_kb)


async def edit_interest(chat_id: int):
    u = await db.query(
        "select User {interest} filter .telegram_id = <str>$telegram_id",
        telegram_id=str(chat_id),
    )
    if not u:
        return
    interest = list(u[0].interest)
    to_edit = (
        await api.send_message(
            chat_id,
            "Выбери категорию, или категории людей, которые тебе интересны",
            reply_markup=gen_interest_kb(interest),
        )
    ).unwrap()
    while True:
        q: CallbackQuery
        q, _ = await bot.dispatch.callback_query.wait_for_answer(chat_id)
        if not q.data.startswith("interest/"):
            continue
        elif q.data == "interest/done":
            if not interest:
                await q.answer("Выбери хотя бы одну категорию")
            else:
                break
        elif q.data == "interest/b":
            if "b" in interest:
                interest.remove("b")
                await q.answer("Парни удалены из категории искомых людей")
            else:
                interest.append("b")
                await q.answer("Парни добавлены в категорию искомых людей")
        elif q.data == "interest/g":
            if "g" in interest:
                interest.remove("g")
                await q.answer("Девушки удалены из категории искомых людей")
            else:
                interest.append("g")
                await q.answer("Девушки добавлены в категорию искомых людей")
        elif q.data == "interest/f":
            if "f" in interest:
                interest.remove("f")
                await q.answer("Друзья удалены из категории искомых людей")
            else:
                interest.append("f")
                await q.answer("Друзья добавлены в категорию искомых людей")
        await api.edit_message_reply_markup(
            chat_id, to_edit.message_id, reply_markup=gen_interest_kb(interest)
        )

    await api.edit_message_text(
        chat_id,
        to_edit.message_id,
        text="Ты выбрал: " + ", ".join([interest_dictionary.get(k) for k in interest]),
    )

    await db.query(
        "update User filter .telegram_id = <str>$telegram_id set {interest := <str>$interest}",
        telegram_id=str(chat_id),
        interest="".join(interest),
    )
    await api.send_message("Предпочтения отредактированы.")


def gen_interest_kb(interest: typing.List[str]):
    return InlineKeyboardMarkup(
        **(
            InlineKeyboard()
            .add(
                InlineButton(
                    "Парни ❤️" if "b" in interest else "Парни",
                    callback_data="interest/b",
                )
            )
            .row()
            .add(
                InlineButton(
                    "Девушки ❤️" if "g" in interest else "Девушки",
                    callback_data="interest/g",
                )
            )
            .row()
            .add(
                InlineButton(
                    "Друзья 💫" if "f" in interest else "Друзья",
                    callback_data="interest/f",
                )
            )
            .add(InlineButton("Готово", callback_data="interest/done"))
            .dict()
        )
    )


interest_dictionary = {"b": "Парней", "g": "Девушек", "f": "Друзей"}


edit_dict = {
    "name": edit_name,
    "age": edit_age,
    "pictures": edit_pictures,
    "description": edit_description,
    "gender": edit_gender,
    "interest": edit_interest,
}


@dataclasses.dataclass
class UserDisplay:
    display: bool


@dp.message(Text(["/profile", "мой профиль"], ignore_case=True))
async def profile(m: Message, user: User):
    await m.answer("Твой профиль:")
    mid = await send_profile(m.chat.id, m.chat.id)
    await m.answer(
        "Доступные действия с профилем:" + ("" if user.display else HIDDEN_PIN),
        reply_markup=get_profile_inline_menu(user),
        reply_to_message_id=mid,
    )
    await send_menu(m.chat.id)


@dp.callback_query(
    FuncRule(lambda cb, _: cb["callback_query"].get("data") == "profile/edit")
)
async def profile_edit(cb: CallbackQuery):
    await cb.ctx_api.edit_message_text(
        cb.from_.id,
        cb.message.message_id,
        text="Что именно ты хочешь отредактировать?",
        reply_markup=KeyboardSet.KEYBOARD_EDIT.get_markup(),
    )
    await cb.answer("Редактируем профиль.")


@dp.callback_query(
    FuncRule(
        lambda cb, _: cb["callback_query"].get("data", "").startswith("profile/edit/")
    )
)
async def profile_edit_field(cb: CallbackQuery):
    field = cb.data.replace("profile/edit/", "", 1)
    u = (
        await db.query(
            "select User {display} filter .telegram_id = <str>$telegram_id",
            telegram_id=str(cb.from_.id),
        )
    )[0]
    if field == "back":
        await cb.ctx_api.edit_message_text(
            cb.from_.id,
            cb.message.message_id,
            text="Доступные действия с профилем:",
            reply_markup=get_profile_inline_menu(u),
        )
        return
    elif field not in edit_dict:
        await cb.answer("Ошибка!")
        return
    await cb.answer("Редактируем.")
    await edit_dict[field](cb.from_.id)
    await profile(Message(**cb.message.dict(), unprep_ctx_api=cb.ctx_api), u)


@dp.callback_query(
    FuncRule(lambda cb, _: cb["callback_query"].get("data") == "profile/toggle_hide")
)
async def profile_hide(cb: CallbackQuery):
    await cb.answer("Меняем настройки доступности профиля профиль.")
    await db.query(
        "update User filter .telegram_id = <str>$telegram_id set { display := not .display }",
        telegram_id=str(cb.from_.id),
    )
    u = (
        await db.query(
            "select User {display} filter .telegram_id = <str>$telegram_id",
            telegram_id=str(cb.from_.id),
        )
    )[0]
    await profile(Message(**cb.message.dict(), unprep_ctx_api=cb.ctx_api), u)
