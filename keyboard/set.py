import typing

from telegrinder import KeyboardSetYAML, Keyboard, InlineKeyboard, InlineButton
from telegrinder.types import ReplyKeyboardRemove, InlineKeyboardMarkup


class KeyboardSet(KeyboardSetYAML):
    __config__ = "keyboard/schemas/keyboards.yaml"

    KEYBOARD_MENU: Keyboard
    KEYBOARD_NEXT: Keyboard
    KEYBOARD_EDIT: InlineKeyboard
    KEYBOARD_UNDO: Keyboard
    KEYBOARD_THATS_ALL: Keyboard
    KEYBOARD_UNDO_EMPTY: Keyboard
    KEYBOARD_GENDER: Keyboard
    KEYBOARD_SKIP: Keyboard
    KEYBOARD_LEAVE_LAST: Keyboard
    KEYBOARD_YN: Keyboard
    KEYBOARD_NOTSET: Keyboard


KeyboardSet.load()

no_kb = ReplyKeyboardRemove(remove_keyboard=True)


def gen_interest_kb(interest: typing.List[str]):
    return (
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
        .get_markup()
    )
