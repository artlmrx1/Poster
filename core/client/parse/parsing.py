from telethon import TelegramClient
from telethon.tl.types import Message, MessageService
import os
import random
import string

async def parse_last_message(channel_username, client: TelegramClient):
    async for message in client.iter_messages(channel_username, limit=1):
        if isinstance(message, Message):
            photo_path = None
            
            if message.photo:
                random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                photo_path = f"./photos/{random_name}.jpg"
                await message.download_media(file=photo_path)
            
            return message, photo_path
        elif isinstance(message, MessageService):
            print(f"Service message encountered in {channel_username}: {message.action}")
            return None, None
        else:
            print(f"Unexpected message type in {channel_username}: {type(message)}")
            return None, None

__all__ = ['parse_last_message']