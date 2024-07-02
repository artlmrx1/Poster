from aiogram import types
from bot.core.microutils.memory import messages
from aiogram.exceptions import TelegramBadRequest

async def reject_handler(call: types.CallbackQuery):
    message_id = call.data.split(':')[1]
    if message_id in messages:
        del messages[message_id]
        try:
            await call.message.delete()
        except TelegramBadRequest as e:
            if "message to delete not found" in str(e).lower():
                pass
            else:
                raise
        await call.answer("Сообщение успешно удалено.", show_alert=True)
    else:
        await call.answer("Сообщение не было найдено в базе.", show_alert=True)