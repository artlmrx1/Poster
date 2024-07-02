from aiogram import Bot
from bot.core.config_manager import config

bot = Bot(token=config["bot"]["token"])