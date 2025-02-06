import telegram.ext as tg_ext
from .loader import TOKEN
from .handlers import setup_all_handlers


class TgBot:
    def __init__(self) -> None:
        self.app = tg_ext.ApplicationBuilder().token(TOKEN).build()

    def run_pooling(self):
        setup_all_handlers(self.app)
        self.app.run_polling()
