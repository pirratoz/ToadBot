from pyrogram.client import Client

from toad_bot.storage.config import NEED_FIX


async def handle_auto_eat_toad(client: Client) -> None:
    chat_id = NEED_FIX
    await client.send_message(
        chat_id=chat_id,
        text="Покормить жабу"
    )
