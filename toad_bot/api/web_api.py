from os import getenv

from aiohttp import (
    ClientSession,
    TCPConnector,
    ClientResponse,
)


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
    async def get_user(self, user_id: int) -> ClientResponse:
        async with self._session.get(f"users/{user_id}") as response:
            return response
