from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.core.microutils.memory import messages
from bot.core.bot import bot
from bot.core.func.handlers.edit_handler import edit_handler
from bot.core.func.handlers.edit_ai_handler import edit_ai_handler
from bot.core.func.handlers.reject_handler import reject_handler
from bot.core.func.handlers.send_handler import send_handler

async def first_interaction_handler(call: types.CallbackQuery, state: FSMContext):
    _, message_id, action = call.data.split(':')
    user_id = call.from_user.id
    
    if message_id in messages and 'sent_messages' in messages[message_id]:
        for uid, mid in messages[message_id]['sent_messages'].items():
            if int(uid) != user_id:
                try:
                    await bot.delete_message(uid, mid)
                except Exception as e:
                    print(f"Failed to delete message for user {uid}: {e}")
        
        del messages[message_id]['sent_messages']
    
    if action == 'medit':
        await edit_handler(call, state)
    elif action == 'edit_ai':
        await edit_ai_handler(call)
    elif action == 'reject':
        await reject_handler(call)
    elif action == 'send':
        await send_handler(call)