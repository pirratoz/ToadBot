from pyrogram.enums import MessageEntityType
from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram import filters


def check_mention() -> bool:
    async def filter_data(self, client: Client, message: Message):
        if not message.entities:
            return False
        
        user = await client.get_me()
        for entitie in message.entities:
            if entitie.type == MessageEntityType.TEXT_MENTION and user.id == entitie.user.id:
                return True
        return False
    return filters.create(filter_data)
