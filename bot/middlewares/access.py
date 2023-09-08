from telegrinder import ABCMiddleware, Message, Keyboard, Button


keyboard = Keyboard().add(Button("/start")).get_markup()


class AccessMiddleware(ABCMiddleware[Message]):
    async def pre(self, m: Message, ctx: dict) -> bool:
        chat = (await m.ctx_api.get_chat(m.chat.id)).unwrap()
        if chat.has_private_forwards:
            await m.answer(
                "⚠️ Привет, чтобы использовать бота нужно убрать ограничение приватности на 'Пересланные сообщения'. Это необходимо сделать чтобы бот смог связать тебя с твоими новыми знакомствами здесь. Как сделаешь - напиши мне слова!",
                reply_markup=keyboard,
            )
            return False
        return True
