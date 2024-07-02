from aiogram import types
from bot.core.microutils.memory import messages
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.core.config_manager import config

async def send_handler(call: types.CallbackQuery):
    message_id = call.data.split(':')[1]
    if message_id not in messages:
        await call.answer("Сообщение не было найдено в базе.", show_alert=True)
        return
    builder = InlineKeyboardBuilder()
    for channel in config['channels']:
        builder.add(types.InlineKeyboardButton(text=f"{channel}", callback_data=f"channel:{message_id}:{channel}"))
    builder.add(types.InlineKeyboardButton(text="Назад", callback_data=f"back:{message_id}"))
    
    try:
        if call.message.content_type == types.ContentType.TEXT:
            await call.message.edit_text("Выберите канал для отправки:", reply_markup=builder.as_markup())
        else:
            await call.message.edit_caption(caption="Выберите канал для отправки:", reply_markup=builder.as_markup())
    except Exception as e:
        await call.answer(f"Ошибка при обновлении сообщения: {str(e)}", show_alert=True)