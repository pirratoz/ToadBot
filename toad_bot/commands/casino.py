from random import choice
from asyncio import sleep

from pyrogram.client import Client
from pyrogram.types import Message


async def handle_casino_click_button(client: Client, message: Message) -> None:
    click_text = choice(["Черный", "Красный"])
    data = {
        "chat_id": message.chat.id,
        "message_id": message.id,
        "callback_data": ""
    }
    for line in message.reply_markup.inline_keyboard:
        for button in line:
            if click_text in button.text:
                data["callback_data"] = button.callback_data
            await sleep(0.333)
            try:
                await client.request_callback_answer(**data)
            except:
                ...
