from pyrogram.client import Client

from toad_bot.storage.config import NEED_FIX


async def handle_cmd_reward_marriage(client: Client) -> None:
    chat_id = NEED_FIX
    await client.send_message(
        chat_id=chat_id,
        text="@toadbot Брак вознаграждение"
    )