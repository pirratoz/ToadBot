from datetime import timedelta

from pyrogram.client import Client

from toad_bot.storage.config import WEB_API
from toad_bot.api.dto import UserProfile
from toad_bot.enums import TaskTypeEnum


async def handle_cmd_toad_day(client: Client) -> None:
    client_me  = await client.get_me()
    client_id = client_me.id

    profile: UserProfile = await WEB_API.get_user(client_id)
    if not profile:
        return
    
    if not profile.user.chat_id:
        return

    await client.send_message(
        chat_id=profile.user.chat_id,
        text="Жаба дня"
    )

    task = next(t for t in profile.tasks if t.task_type == TaskTypeEnum.FROG_DAY)

    time_delta = timedelta(days=1)

    json_data = {
        "user_id": client_id,
        "type": TaskTypeEnum.FROG_DAY,
        "next_run": task.next_run + time_delta,
    }

    await WEB_API.set_next_run(**json_data)
