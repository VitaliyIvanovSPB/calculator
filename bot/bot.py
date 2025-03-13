import asyncio
import logging
import requests
from telegram.ext import Application

from .loader import TOKEN
from .handlers import setup_all_handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

class TGBot:
    def __init__(self):
        self.token = TOKEN
        self.application = None


    async def initialize(self):
        logger.info("Initializing the bot...")

        try:
            # Build the application using the token
            self.application = Application.builder().token(self.token).build()
            setup_all_handlers(self.application)

            # Initialize the application
            await self.application.initialize()
            await self.application.start()

            # Start polling
            await self.application.updater.start_polling()

            # Keep the bot running
            while True:
                await asyncio.sleep(3600)

        except asyncio.CancelledError:
            logger.info("Bot shutdown requested")

    async def start(self):
        await self.initialize()

    async def stop(self):
        if self.application:
            await self.application.stop()

def send_message(user_id, data):
        try:
            response = requests.post(
                url,
                json={
                    "chat_id": user_id,
                    "text": data,
                },
                timeout=10
            )
            response.raise_for_status()  # Проверка на ошибки HTTP
            return "Сообщение успешно отправлено!"
        except requests.exceptions.RequestException as e:
            return f"Ошибка при отправке сообщения: {e}"


