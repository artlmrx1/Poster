from aiogram import types
from bot.core.microutils.memory import messages
from bot.core.config_manager import config
import os

async def channel_handler(call: types.CallbackQuery):
    _, message_id, channel = call.data.split(':')
    if message_id not in messages:
        await call.answer("Сообщение не было найдено в базе.", show_alert=True)
        return
    
    text = messages[message_id]['text']
    photo_path = messages[message_id].get('photo_path')
    
    if photo_path and os.path.exists(photo_path):
        if len(text) > 1024:
            await call.answer("Сообщение слишком длинное. Пожалуйста, сократите его до 1024 символов или меньше.", show_alert=True)
            return
    elif len(text) > 4096:
        await call.answer("Сообщение слишком длинное. Пожалуйста, сократите его до 4096 символов или меньше.", show_alert=True)
        return

    try:
        from bot.core.parser import client
        if not client.is_connected():
            await client.connect()
        if not await client.is_user_authorized():
            await call.answer("Client is not authorized. Please restart the bot.", show_alert=True)
            return
        
        message_sent = False
        if photo_path and os.path.exists(photo_path):
            caption = text[:1024]
            await client.send_file(channel, photo_path, caption=caption, parse_mode='html')
            message_sent = True
        else:
            await client.send_message(channel, text, parse_mode='html')
            message_sent = True
        
        if message_sent:
            del messages[message_id]
            success_text = f"Сообщение успешно отправлено в канал ✅: @{channel}"
            if call.message.content_type == types.ContentType.TEXT:
                await call.message.edit_text(success_text)
            else:
                await call.message.edit_caption(caption=success_text)
            await call.answer(f"Сообщение успешно отправлено в канал ✅: @{channel}", show_alert=True)
    except Exception as e:
        print(f"Error in channel_handler: {e}")
        await call.answer(f"Ошибка при отправке сообщения: {str(e)}", show_alert=True)
    finally:
        if client and client.is_connected():
            await client.disconnect()