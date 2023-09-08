from .bot import bot

import tasks.notify
import asyncio

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(bot.run_polling())
    loop.create_task(tasks.notify.notify_task())
    loop.run_forever()
