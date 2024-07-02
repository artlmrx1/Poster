from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.core.microutils.memory import messages
from bot.core.func.send_message import send_message_to_user
from bot.core.microutils.convertor_html import apply_entities_to_text
from bot.core.bot import bot
import random
import string
import os

async def post_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    post = message.caption if message.caption else message.text
    entities = message.caption_entities if message.caption_entities else message.entities
    data = await state.get_data()
    message_id = data.get('message_id')
    edit_message_id = data.get('edit_message_id')
    
    if message_id not in messages:
        await message.answer("Это сообщение больше недоступно для редактирования.")
        await state.clear()
        await message.delete()
        return

    post = apply_entities_to_text(post, entities)
    
    photo = message.photo[-1] if message.photo else None
    if photo:
        file_id = photo.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        download_path = f"./photos/{random_name}.jpg"
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        await bot.download_file(file_path, download_path)
        messages[message_id]['photo_path'] = download_path
    else:
        messages[message_id]['photo_path'] = None

    messages[message_id]['text'] = post
    messages[message_id]['entities'] = entities
    
    await send_message_to_user(message_id, post, messages[message_id]['photo_path'], user_id)
    await state.clear()
    
    await message.delete()
    
    if edit_message_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=edit_message_id)
        except Exception as e:
            print(f"Error deleting edit message: {e}")