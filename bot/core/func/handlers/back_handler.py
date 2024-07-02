from aiogram import types
from bot.core.microutils.memory import messages
from bot.core.bot import bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def back_handler(call: types.CallbackQuery):
    message_id = call.data.split(':')[1]
    if message_id in messages:
        text = messages[message_id]['text']
        photo_path = messages[message_id].get('photo_path')

        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Изменить", callback_data=f"first_interaction:{message_id}:medit"))
        builder.add(types.InlineKeyboardButton(text="Изменить ИИ", callback_data=f"first_interaction:{message_id}:edit_ai"))
        builder.add(types.InlineKeyboardButton(text="Отклонить", callback_data=f"first_interaction:{message_id}:reject"))
        builder.add(types.InlineKeyboardButton(text="Отправить", callback_data=f"first_interaction:{message_id}:send"))
        builder.adjust(2).as_markup()
        
        try:
            await call.message.delete()
            
            if photo_path:
                await bot.send_photo(call.message.chat.id, types.FSInputFile(photo_path), caption=text, reply_markup=builder.as_markup(), parse_mode='HTML')
            else:
                await bot.send_message(call.message.chat.id, text, reply_markup=builder.as_markup(), parse_mode='HTML')
        except Exception as e:
            print(f"Error in back_handler: {e}")
            await call.answer("Произошла ошибка при обновлении сообщения. Попробуйте еще раз или обратитесь к администратору.", show_alert=True)
    else:
        await call.answer("Это сообщение больше недоступно.", show_alert=True)