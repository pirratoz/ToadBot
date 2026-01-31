from pyrogram.client import Client
from pyrogram.types import Message

import toad_bot.storage.config as config


async def handle_set_chat_info(client: Client, message: Message) -> None:
    me = await client.get_me()
    status = await config.WEB_API.set_info_chat(
        user_id=me.id,
        chat_id=message.chat.id,
        chat_title=message.chat.title
    )
    await message.reply(text=["Ошибка", "Установил"][status])
