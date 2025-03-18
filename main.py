import asyncio
from bot import TGBot

def run():
    bot = TGBot()
    asyncio.run(bot.start())

if __name__ == '__main__':
    run()