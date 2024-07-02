from bot.core.config_manager import config
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from bot.core.state import PostForm
from bot.core.parser import parse_messages
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
import asyncio
from bot.core.func.handlers.post_handler import post_handler
from bot.core.func.handlers.edit_handler import edit_handler
from bot.core.func.handlers.edit_ai_handler import edit_ai_handler
from bot.core.func.handlers.reject_handler import reject_handler
from bot.core.func.handlers.send_handler import send_handler
from bot.core.func.handlers.channel_handler import channel_handler
from bot.core.func.first_interaction import first_interaction_handler
from bot.core.func.handlers.back_handler import back_handler
from bot.core.bot import bot
from bot.core.func.handlers.edit_ai_handler import ai_edit_handler, ai_apply_handler, ai_regenerate_handler, ai_cancel_handler

dp = Dispatcher(storage=MemoryStorage())    

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    if str(message.from_user.id) in config["user_ids"]:
        await message.answer("Бот запущен и готов к работе!")
    else:
        pass

@dp.message(StateFilter(PostForm.post))
async def process_seed_handler(message: types.Message, state: FSMContext):
    await post_handler(message, state)

dp.callback_query(lambda c: c.data.startswith("medit:"))(edit_handler)
dp.callback_query(lambda c: c.data.startswith("edit_ai:"))(edit_ai_handler)
dp.callback_query(lambda c: c.data.startswith("reject:"))(reject_handler)
dp.callback_query(lambda c: c.data.startswith("send:"))(send_handler)
dp.callback_query(lambda c: c.data.startswith("channel:"))(channel_handler)
dp.callback_query(lambda c: c.data.startswith("first_interaction:"))(first_interaction_handler)
dp.callback_query(lambda c: c.data.startswith("back:"))(back_handler)
dp.callback_query(lambda c: c.data.startswith("ai_edit_preview:"))(ai_edit_handler)
dp.callback_query(lambda c: c.data.startswith("ai_apply:"))(ai_apply_handler)
dp.callback_query(lambda c: c.data.startswith("ai_regenerate:"))(ai_regenerate_handler)
dp.callback_query(lambda c: c.data.startswith("ai_cancel:"))(ai_cancel_handler)

async def main() -> None:
    parse_task = asyncio.create_task(parse_messages(bot))
    try:
        await dp.start_polling(bot)
    finally:
        parse_task.cancel()
        try:
            await parse_task
        except asyncio.CancelledError:
            pass