from . import auth, bot, app, uni, data

routers = (auth.router, bot.router, app.router, uni.router, data.router)
