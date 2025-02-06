import logging

from bot import TgBot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    TgBot().run_pooling()


if __name__ == '__main__':
    run()
