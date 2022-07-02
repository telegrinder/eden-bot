from telegrinder import Dispatch, CallbackQuery

import database.like
from client import logger
from logic import REPORT_RECEIVED

dp = Dispatch()


@dp.callback_query(REPORT_RECEIVED)
async def report(cb: CallbackQuery):
    await cb.answer("Жалоба будет рассмотрена в ближайшее время")
    uid = cb.data.replace("report/", "", 1)
    await database.user.add_report(uid)
    await cb.ctx_api.delete_message(cb.message.chat.id, cb.message.message_id)
    logger.info(f"{cb.from_.first_name} reported {uid}")
