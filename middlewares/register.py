import typing

from keyboard.keyboard import KeyboardSet, no_kb, gen_interest_kb
import database
from client import logger, bot
from telegrinder import (
    ABCMiddleware,
    Message,
    Keyboard,
    Button,
    CallbackQuery,
)
from telegrinder.types import InputMediaPhoto
from telegrinder.bot.rules import FuncRule, Text
from tools import send_menu

interest_dictionary = {"b": "Парней", "g": "Девушек", "f": "Друзей"}


class RegisterMiddleware(ABCMiddleware):
    async def pre(self, m: Message, ctx: dict) -> bool:
        users = await database.user.get_full(m.chat.id)
        if not users:
            logger.info(f"Registering {m.from_.first_name} ({m.from_.id})")
            await m.reply(
                "Привет, кажется это наша первая встреча, "
                "поэтому, предлагаю приступить к оформлению анкеты"
            )
            name_kb = (
                Keyboard(resize_keyboard=True)
                .add(Button(m.from_.first_name))
                .get_markup()
            )
            await m.answer("Как мне к тебе обращаться?", reply_markup=name_kb)

            name: str
            while True:
                m2, _ = await bot.dispatch.message.wait_for_message(m.chat.id)
                if not m2.text:
                    await m2.reply(
                        "Пожалуйста, напиши как мне к тебе обращаться.",
                        reply_markup=name_kb,
                    )
                else:
                    name = m2.text
                    break

            await m.answer(
                f"Хорошо, {name}. Теперь пожалуйста напиши твой возраст.",
                reply_markup=no_kb,
            )
            m2, _ = await bot.dispatch.message.wait_for_message(
                m.chat.id,
                FuncRule(
                    lambda event, _: event["message"]["text"]
                    and event["message"]["text"].isdigit()
                    and 15 <= int(event["message"]["text"]) <= 100
                ),
                default="Пожалуйста напиши возвраст числом, учти, что анкету "
                "можно создавать, как минимум достигнув возраста 15 лет",
            )
            age = int(m2.text)

            await m.answer(
                "Определимся с полом, ты парень или девушка?",
                reply_markup=KeyboardSet.KEYBOARD_GENDER.get_markup(),
            )
            m3, _ = await bot.dispatch.message.wait_for_message(
                m.chat.id,
                Text(["парень", "девушка"], ignore_case=True),
                default="Выбери либо «парень», либо «девушка»",
            )

            gender = 0 if m3.text.lower() == "парень" else 1

            to_edit = (
                await m.answer(
                    "Выбери категорию, или категории людей, которые тебе интересны",
                    reply_markup=gen_interest_kb([]),
                )
            ).unwrap()

            interest = []
            while True:
                q: CallbackQuery
                q, _ = await bot.dispatch.callback_query.wait_for_answer(m.chat.id)
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
                await m.ctx_api.edit_message_reply_markup(
                    m.chat.id,
                    to_edit.message_id,
                    reply_markup=gen_interest_kb(interest),
                )

            await m.ctx_api.edit_message_text(
                m.chat.id,
                to_edit.message_id,
                text="Ты выбрал: "
                + ", ".join([interest_dictionary.get(i) for i in interest]),
            )
            await m.ctx_api.edit_message_reply_markup(
                m.chat.id, to_edit.message_id, reply_markup=no_kb
            )
            await m.answer(
                f"Теперь пожалуйста пришли фотографию для твоего профиля.",
                reply_markup=KeyboardSet.KEYBOARD_LEAVE_LAST.get_markup(),
            )

            photos: typing.List[str] = []
            while len(photos) < 3:
                ph_m, _ = await bot.dispatch.message.wait_for_message(
                    m.chat.id,
                    FuncRule(
                        lambda event, _: (
                            event["message"].get("text")
                            and (
                                event["message"]["text"].lower()
                                in ("это все", "это всё")
                                and len(photos)
                                or event["message"]["text"].lower()
                                == "оставить прошлую"
                            )
                        )
                        or event["message"]["photo"]
                    ),
                    default="Пришли фотографию для твоего профиля",
                )
                if ph_m.text and ph_m.text.lower() in (
                    "это все",
                    "это всё",
                    "оставить прошлую",
                ):
                    if ph_m.text.lower() == "оставить прошлую":
                        photos = [
                            p.file_id
                            for p in await database.picture.get_profile_pictures(
                                m.chat.id
                            )
                        ]
                        if not photos:
                            await m.answer(
                                "К сожалению у меня не сохранено твоих фотографий, придется загрузить новую",
                                reply_markup=no_kb,
                            )
                            continue
                    break
                photos.append(ph_m.photo[-1].file_id)
                if len(photos) < 3:
                    await m.answer(
                        "Добавил, пришли мне еще, если хочешь добавить "
                        "еще фотографию в профиль, или напиши «это все».",
                        reply_markup=KeyboardSet.KEYBOARD_THATS_ALL.get_markup(),
                    )

            await m.answer(
                "Расскажи немного о себе, или, если не хочешь, ты можешь пропустить этот шаг.",
                reply_markup=KeyboardSet.KEYBOARD_SKIP.get_markup(),
            )

            description: typing.Optional[str]
            dm, _ = await bot.dispatch.message.wait_for_message(m.chat.id)
            if not dm.text or dm.text.lower() in ("пропустить",):
                await dm.reply("Хорошо, не будем добавлять описание")
                description = None
            else:
                description = dm.text

            await m.answer("Все готово, вот твоя анкета:", reply_markup=no_kb)
            await m.ctx_api.send_media_group(
                m.chat.id,
                [
                    InputMediaPhoto(
                        type="photo",
                        media=photo,
                        caption=(
                            f"{name}, {age}"
                            if not description
                            else f"{name}, {age} – {description}"
                        )
                        if i == 0
                        else None,
                    )
                    for i, photo in enumerate(photos)
                ],
            )

            await m.answer(
                "Все правильно?", reply_markup=KeyboardSet.KEYBOARD_YN.get_markup()
            )

            cm, _ = await bot.dispatch.message.wait_for_message(
                m.chat.id,
                Text(["Да", "Нет"], ignore_case=True),
                default="Подтверди (Да) или отмени (Нет) создание профиля",
            )

            if cm.text.lower() == "да":
                await m.answer("Отлично, все готово", reply_markup=no_kb)
                await database.picture.delete_by_user(m.from_.id)
                await database.picture.insert_many(m.from_.id, photos)
                users = await database.user.new(
                    m.from_.id,
                    name=name,
                    age=age,
                    gender=gender,
                    interest="".join(interest),
                    description=description or "",
                )
                ctx.update({"user": users[0]})
                logger.info(f"Registration completed {m.chat.first_name}")
                await send_menu(m.chat.id)

            else:
                await cm.answer(
                    "Напиши любое сообщение, чтобы начать заполнение заново"
                )

            return False
        ctx.update({"user": users[0]})
        return True
