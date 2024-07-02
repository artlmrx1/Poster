from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.core.microutils.memory import messages
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.core.state import PostForm

async def edit_handler(call: types.CallbackQuery, state: FSMContext):
    message_id = call.data.split(':')[1]
    if message_id in messages:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Назад", callback_data=f"back:{message_id}"))
        
        if call.message.content_type == types.ContentType.TEXT:
            edit_message = await call.message.edit_text("Пришлите измененное сообщение с фото:", reply_markup=builder.as_markup())
        else:
            edit_message = await call.message.edit_caption(caption="Пришлите измененное сообщение с фото:", reply_markup=builder.as_markup())
        
        await state.set_state(PostForm.post)
        await state.update_data(message_id=message_id, edit_message_id=edit_message.message_id)
    else:
        await call.answer("Это сообщение больше недоступно для редактирования.", show_alert=True)