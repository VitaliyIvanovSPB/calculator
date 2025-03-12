import asyncio
import logging

from telegram.ext import Application

from .loader import TOKEN
from .handlers import setup_all_handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def run_bot():
    logger.info("Starting the bot...")

    application = None
    try:
        application = Application.builder().token(TOKEN).build()
        setup_all_handlers(application)

        # Явная инициализация
        await application.initialize()
        await application.start()

        # Запускаем поллинг
        await application.updater.start_polling()

        # Бесконечный цикл ожидания
        while True:
            await asyncio.sleep(3600)

    except asyncio.CancelledError:
        print("Bot shutdown requested")
