from aiogram import types
from bot.core.microutils.memory import messages
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.core.func.send_message import send_message_to_user
from bot.core.ai_edit.gbt_editer import edit_message_with_ai
from bot.core.ai_edit.prompt import get_prompt_news, get_prompt_calls, get_prompt_ton_news, get_prompt_sol
from bot.core.func.handlers.back_handler import back_handler
from aiogram.exceptions import TelegramBadRequest
from bot.core.bot import bot

async def edit_ai_handler(call: types.CallbackQuery):
    message_id = call.data.split(':')[1]
    if message_id not in messages:
        await call.answer("Сообщение не было найдено в базе.", show_alert=True)
        return
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="NEWS", callback_data=f"ai_edit_preview:{message_id}:news"))
    builder.add(types.InlineKeyboardButton(text="CALLS", callback_data=f"ai_edit_preview:{message_id}:calls"))
    builder.add(types.InlineKeyboardButton(text="FIRST TON NEWS", callback_data=f"ai_edit_preview:{message_id}:ton_news"))
    builder.add(types.InlineKeyboardButton(text="SOL", callback_data=f"ai_edit_preview:{message_id}:sol"))
    builder.add(types.InlineKeyboardButton(text="Назад", callback_data=f"back:{message_id}"))
    builder.adjust(2).as_markup()
    
    try:
        if call.message.content_type == types.ContentType.TEXT:
            await call.message.edit_text("Выберите целевой промпт:", reply_markup=builder.as_markup())
        else:
            await call.message.edit_caption(caption="Выберите целевой промпт:", reply_markup=builder.as_markup())
    except Exception as e:
        await call.answer(f"Ошибка при обновлении сообщения: {str(e)}", show_alert=True)

async def ai_edit_handler(call: types.CallbackQuery):
    _, message_id, prompt_type = call.data.split(':')
    if message_id not in messages:
        await call.answer("Сообщение не было найдено в базе.", show_alert=True)
        return
    
    if messages[message_id]['ai_text'] == messages[message_id]['text']:
        text = messages[message_id]['ai_text']
    else:
        text = messages[message_id]['text']

    photo_path = messages[message_id].get('photo_path')
    
    try:
        if call.message.content_type == types.ContentType.TEXT:
            await call.message.edit_text("Изменение ИИ... ⚙️")
        else:
            await call.message.edit_caption(caption="Изменение ИИ... ⚙️")
    except Exception as e:
        await call.answer(f"Ошибка при обновлении сообщения: {str(e)}", show_alert=True)
        return

    if prompt_type == 'news':
        prompt = await get_prompt_news(text)
    elif prompt_type == 'calls':
        prompt = await get_prompt_calls(text)
    elif prompt_type == 'ton_news':
        prompt = await get_prompt_ton_news(text)
    elif prompt_type == 'sol':
        prompt = await get_prompt_sol(text)
    new_text = await edit_message_with_ai(prompt)
    
    if new_text == "error":
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Назад", callback_data=f"back:{message_id}"))
        if call.message.content_type == types.ContentType.TEXT:
            await call.message.edit_text("Извините, произошла ошибка при обработке текста...", reply_markup=builder.as_markup())
        else:
            await call.message.edit_caption(caption="Извините, произошла ошибка при обработке текста...", reply_markup=builder.as_markup())
    else:
        await call.message.delete()
        messages[message_id]['ai_text'] = new_text
        
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Применить", callback_data=f"ai_apply:{message_id}"))
        builder.add(types.InlineKeyboardButton(text="Перегенерировать", callback_data=f"ai_regenerate:{message_id}:{prompt_type}"))
        builder.add(types.InlineKeyboardButton(text="Отмена", callback_data=f"ai_cancel:{message_id}"))
        builder.adjust(2).as_markup()

        try:
            if photo_path:
                await bot.send_photo(call.from_user.id, types.FSInputFile(photo_path), caption=new_text, reply_markup=builder.as_markup(), parse_mode='HTML')
            else:
                await bot.send_message(call.from_user.id, new_text, reply_markup=builder.as_markup(), parse_mode='HTML')
        except Exception:
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(text="Назад", callback_data=f"back:{message_id}"))
            await bot.send_message(call.from_user.id, 'Извините, произошла ошибка при генерации...', reply_markup=builder.as_markup(), parse_mode='HTML')

async def ai_apply_handler(call: types.CallbackQuery):
    message_id = call.data.split(':')[1]
    messages[message_id]['text'] = messages[message_id]['ai_text']
    await send_message_to_user(message_id, messages[message_id]['text'], messages[message_id].get('photo_path'), call.from_user.id)

async def ai_regenerate_handler(call: types.CallbackQuery):
    _, message_id, prompt_type = call.data.split(':')
    await ai_edit_handler(call)

async def ai_cancel_handler(call: types.CallbackQuery):
    message_id = call.data.split(':')[1]
    await back_handler(call)
