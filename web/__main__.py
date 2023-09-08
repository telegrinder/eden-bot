from web.application import app
from bot.bot import bot
import asyncio
import uvicorn

if __name__ == "__main__":

    @app.on_event("startup")
    async def startup_event() -> None:
        asyncio.get_running_loop().create_task(
            bot.run_polling(skip_updates=True),
        )

    uvicorn.run(app)
