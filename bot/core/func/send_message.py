from bot.core.microutils.convertor_html import markdown_to_html
from bot.core.microutils.memory import messages
from bot.core.config_manager import config
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram import types
from bot.core.bot import bot

async def send_message_to_users(bot, message_id, message, photo_path):
    sent_messages = {}
    for user_id in config['user_ids']:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Изменить", 
            callback_data=f"first_interaction:{message_id}:medit")
        )
        builder.add(types.InlineKeyboardButton(text="Изменить ИИ", callback_data=f"first_interaction:{message_id}:edit_ai"))
        builder.add(types.InlineKeyboardButton(text="Отклонить", callback_data=f"first_interaction:{message_id}:reject"))
        builder.add(types.InlineKeyboardButton(text="Отправить", callback_data=f"first_interaction:{message_id}:send"))
        builder.adjust(2).as_markup()
        
        text = markdown_to_html(message.text)
        
        if photo_path:
            sent_message = await bot.send_photo(
                chat_id=user_id,
                photo=types.FSInputFile(photo_path),
                caption=text,
                parse_mode='HTML',
                reply_markup=builder.as_markup()
            )
        else:
            sent_message = await bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode='HTML',
                reply_markup=builder.as_markup()
            )
        sent_messages[user_id] = sent_message.message_id

    
    messages[message_id] = {
        'text': text,
        'ai_text': text,
        'photo_path': photo_path,
        'sent_messages': sent_messages,
        'entities': message.entities
    }

async def send_message_to_user(message_id, text, photo_path, user_id_starter):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Изменить", callback_data=f"medit:{message_id}"))
    builder.add(types.InlineKeyboardButton(text="Изменить ИИ", callback_data=f"edit_ai:{message_id}"))
    builder.add(types.InlineKeyboardButton(text="Отклонить", callback_data=f"reject:{message_id}"))
    builder.add(types.InlineKeyboardButton(text="Отправить", callback_data=f"send:{message_id}"))
    builder.adjust(2).as_markup()

    try:
        if photo_path:
            await bot.send_photo(user_id_starter, types.FSInputFile(photo_path), caption=text, reply_markup=builder.as_markup(), parse_mode='HTML')
        else:
            await bot.send_message(user_id_starter, text, reply_markup=builder.as_markup(), parse_mode='HTML')
    except Exception as e:
        print(f"Error in send_message_to_user: {e}")
        if isinstance(e, TelegramBadRequest) and "message caption is too long" in str(e):
            old_text = messages[message_id].get('text', 'Error: Old text not found')
            if photo_path:
                await bot.send_photo(user_id_starter, types.FSInputFile(photo_path), caption=old_text, reply_markup=builder.as_markup(), parse_mode='HTML')
            else:
                await bot.send_message(user_id_starter, old_text, reply_markup=builder.as_markup(), parse_mode='HTML')
        else:
            if photo_path:
                await bot.send_photo(user_id_starter, types.FSInputFile(photo_path), caption=text, reply_markup=builder.as_markup(), parse_mode='HTML')
            else:
                await bot.send_message(user_id_starter, text, reply_markup=builder.as_markup(), parse_mode='HTML')
           
         