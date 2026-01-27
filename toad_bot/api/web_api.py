from os import getenv

from aiohttp import (
    ClientSession,
    TCPConnector,
)

from toad_bot.api.dto import UserProfile
from toad_bot.api.dto.user_profile import TaskInfo


class WebApi:
    def __init__(self):
        self._session: ClientSession | None = None
        self._web_api_key = getenv("WEB_API_KEY", "NotSetup")
        self._base_url = getenv("WEB_API_URL", "NotSetup")

    def ensure_session(func):
        async def wrapper(self: "WebApi", *args, **kwargs):
            if not self._session or self._session.closed:
                connector = TCPConnector(verify_ssl=False)
                self._session = ClientSession(
                    base_url=self._base_url,
                    headers={"Web-API-Key": self._web_api_key},
                    connector=connector
                )
            return await func(self, *args, **kwargs)
        return wrapper
    
    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
    
    @ensure_session
    async def get_user(self, user_id: int) -> UserProfile | None:
        async with self._session.get(f"users/{user_id}") as response:
            if response.status == 200:
                return UserProfile.load_from_json(await response.json())
            return None

    @ensure_session
    async def get_ready_tasks(self, user_ids: list[int]) -> list[TaskInfo] | None:
        json_data = {
            "user_ids": user_ids
        }
        async with self._session.post("tasks/ready", json=json_data) as response:
            if response.status == 200:
                res = await response.json()
                return TaskInfo.load_from_jsons(res["tasks"])
            return None