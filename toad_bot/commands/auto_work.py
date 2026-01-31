from asyncio import sleep

from pyrogram.client import Client

import toad_bot.storage.config as config
from toad_bot.api.dto import UserProfile
from toad_bot.enums import (
    TaskTypeEnum,
    WorkTypeEnum,
)
from toad_bot.commands.work_delay import (
    WorkTimeDelaySec,
    CafeteriaWork,
    CasinoWork,
    CookWork,
    CroupierWork,
    RobberWork,
)


async def check_work_on(client_id: int) -> bool:
    profile: UserProfile = await config.WEB_API.get_user(client_id)
    task = next(t for t in profile.tasks if t.task_type == TaskTypeEnum.WORK)
    return task.turn


async def handle_cmd_work(client: Client) -> None:
    client_me  = await client.get_me()
    client_id = client_me.id

    profile: UserProfile = await config.WEB_API.get_user(client_id)
    if not profile:
        return
    
    if not profile.user.chat_id:
        return
    
    work_table: dict[WorkTypeEnum, WorkTimeDelaySec] = {
        WorkTypeEnum.CAFETERIA: CafeteriaWork,
        WorkTypeEnum.CASINO: CasinoWork,
        WorkTypeEnum.COOK: CookWork,
        WorkTypeEnum.CROUPIER: CroupierWork,
        WorkTypeEnum.ROBBER: RobberWork,
    }

    task = next(t for t in profile.tasks if t.task_type == TaskTypeEnum.WORK)

    work_type = WorkTypeEnum(task.extra.get("type", WorkTypeEnum.CAREFREE.value))
    if work_type == WorkTypeEnum.CAREFREE:
        return
    
    work = work_table[work_type]

    time_delta = work.next_work_delay()

    json_data = {
        "user_id": client_id,
        "type": TaskTypeEnum.WORK,
        "next_run": task.next_run + time_delta,
    }

    await config.WEB_API.set_next_run(**json_data)

    send_message = lambda text: client.send_message(chat_id=profile.user.chat_id, text=text)

    await send_message(text=work.command)

    if work.walk_to_work > 0:
        await sleep(work.walk_to_work)
        if not await check_work_on(client_id):
            return
        await send_message(text="Начать работу")

    await sleep(work.work_time)
    if not await check_work_on(client_id):
        return
    await send_message(text="@toadbot Завершить работу")
