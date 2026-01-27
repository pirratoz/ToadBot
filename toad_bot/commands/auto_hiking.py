from random import choice
from asyncio import sleep

from pyrogram.client import Client
from pyrogram.types import Message


async def handle_hiking_click_button(client: Client, message: Message) -> None:
    if not message.reply_markup.inline_keyboard:
        return
    
    await client.send_message(
        chat_id=message.chat.id,
        text="Реанимировать жабу"
    )
    await sleep(0.566)
    data = {
        "chat_id": message.chat.id,
        "message_id": message.id,
        "callback_data": choice(message.reply_markup.inline_keyboard[0]).callback_data
    }

    try:
        await client.request_callback_answer(**data)
    except:
        ...
