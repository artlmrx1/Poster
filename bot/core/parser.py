from bot.core.func.send_message import send_message_to_users
from core.client.parse.parsing import parse_last_message
from core.client.client_core import create_client
from bot.core.microutils.memory import messages
from bot.core.config_manager import config
from aiogram import Bot
import asyncio

parsed_messages = []

async def parse_messages(bot: Bot):
    global client
    while True:
        session_name = f"./sessions/{config['phone_number']}"
        client = await create_client(session_name, config['api_id'], config['api_hash'], config['phone_number'])
        async with client:
            print('Начало парсинга')
            while True:
                for channel in config['channels_parse']:
                    message, photo_path = await parse_last_message(channel, client)
                    if message is None and photo_path is None:
                        print(f"Пропуск канала {channel}: не удалось получить сообщение")
                        continue
                    if message and message.text not in parsed_messages:
                        parsed_messages.append(message.text)
                        message_id = str(len(messages) + 1)
                        
                        if photo_path:
                            print(f"Photo downloaded: {photo_path}")
                        
                        messages[message_id] = {'message': message, 'photo_path': photo_path}
                        await send_message_to_users(bot, message_id, message, photo_path)
                        print(f'Сообщение обработано: {message.text[:50]}...')
                    else:
                        print(f"Пропуск канала {channel}: сообщение уже обработано или пустое")
                await asyncio.sleep(60)