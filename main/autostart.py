import asyncio

from aiogram import Bot, Dispatcher

from service.data import config
from service.Bot.handlers import router
from service.Bot.markups import inlinemarkups

dp = Dispatcher()
bot = Bot(config.BOT_TOKEN)

dp.include_router(router)


async def start_bot():
    while True:
        try:
            for tg_id in config.TELEGRAM_IDS:
                await bot.send_message(tg_id, "<b>Установлено соединение с вашим ПК</b>",
                                       parse_mode="HTML",
                                       reply_markup=inlinemarkups.pc_start_markup)

            await dp.start_polling(bot)
            continue
        except:
            pass

asyncio.run(start_bot())
