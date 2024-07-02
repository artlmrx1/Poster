from bot.bot_main import main

import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs('logs', exist_ok=True)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

file_handler = RotatingFileHandler('logs/bot.log', maxBytes=10*1024*1024, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
console_handler.setLevel(logging.INFO)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)
logger.info("Logging has been set up")

logging.getLogger('aiogram').setLevel(logging.DEBUG)
logging.getLogger('aiosqlite').setLevel(logging.DEBUG)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())