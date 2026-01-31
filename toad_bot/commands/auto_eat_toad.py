from datetime import timedelta

from pyrogram.client import Client

import toad_bot.storage.config as config
from toad_bot.api.dto import UserProfile
from toad_bot.enums import TaskTypeEnum


async def handle_auto_eat_toad(client: Client) -> None:
    client_me  = await client.get_me()
    client_id = client_me.id

    profile: UserProfile = await config.WEB_API.get_user(client_id)
    if not profile:
        return
    
    if not profile.user.chat_id:
        return
    
    await client.send_message(
        chat_id=profile.user.chat_id,
        text="Покормить жабу"
    )

    task = next(t for t in profile.tasks if t.task_type == TaskTypeEnum.EAT_FROG)

    time_delta = timedelta(hours=12, minutes=2)
    if profile.user.is_vip:
        time_delta = timedelta(hours=6, minutes=2)

    json_data = {
        "user_id": client_id,
        "type": TaskTypeEnum.EAT_FROG,
        "next_run": task.next_run + time_delta,
    }

    await config.WEB_API.set_next_run(**json_data)

