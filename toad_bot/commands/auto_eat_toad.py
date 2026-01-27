from pyrogram.client import Client

from toad_bot.storage.config import WEB_API
from toad_bot.api.dto import UserProfile


async def handle_auto_eat_toad(client: Client) -> None:
    client_me  = await client.get_me()
    client_id = client_me.id

    profile: UserProfile = await WEB_API.get_user(client_id)
    if not profile:
        return
    
    if not profile.user.chat_id:
        return
    
    await client.send_message(
        chat_id=profile.user.chat_id,
        text="Покормить жабу"
    )
