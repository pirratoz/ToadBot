from pathlib import Path
from os import (
    getenv,
    makedirs,
    path
)
from asyncio import (
    sleep as asyncio_sleep,
    create_task as asyncio_create_task,
)

from pyrogram import (
    Client,
    errors,
)

from toad_bot.enums import (
    AuthInfoEnum,
    TaskTypeEnum,
)
from toad_bot.storage import config
from toad_bot.handlers import init_handlers
from toad_bot.commands import (
    handle_cmd_reward_marriage,
    handle_cmd_reward_clan,
    handle_auto_eat_baby_toad,
    handle_auto_eat_toad,
    handle_cmd_toad_day,
    handle_cmd_work,
)


class AuthInfo:
    def __init__(self):
        self.clients: dict[int, Client] = {}
        self.hash_code: dict[int, str] = {}
        self.client_running: dict[int, bool] = {}
    
    def add_client(
        self,
        user_id: int,
        api_id: int,
        api_hash: str,
        password_2fa: str,
        phone: str
    ) -> Client:
        path_sessions = Path(getenv("PATH_TG_BOT_SESSIONS"))
        path_user = path_sessions / f"{user_id}"
        if not path.exists(path_sessions):
            makedirs(path_sessions)
        if not path.exists(path_user):
            makedirs(path_user)
        client = Client(
            name=f"{path_user}/user",
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone,
            password=password_2fa,
            device_model=config.DEVICE_MODEL,
            app_version=config.APP_VERSION,
            system_version=config.SYSTEM_VERSION,
        )
        self.clients[user_id] = client
        init_handlers(client)
        self.client_running[user_id] = False
        return client
    
    def remove_files(self, user_id: int) -> None:
        path_sessions = Path(getenv("PATH_TG_BOT_SESSIONS"))
        path_user = path_sessions / f"{user_id}"
        for file in path_user.iterdir():
            try:
                if file.is_file():
                    file.unlink(missing_ok=True)
            except Exception as e:
                ...
        path_user.rmdir()

    def get_client(self, user_id: int) -> Client | None:
        return self.clients.get(user_id, None)
    
    def get_hash_code(self, user_id: int) -> str | None:
        return self.hash_code.get(user_id, None)

    async def is_auth(self, user_id: int) -> AuthInfoEnum:
        client = self.get_client(user_id)
        if not client:
            return AuthInfoEnum.CLIENT_NOT_FOUND
        
        status = await client.connect()
        await client.disconnect()

        if status:
            return AuthInfoEnum.CLIENT_AUTH_SUCCSESS

        return AuthInfoEnum.CLIENT_AUTH_WRONG
    
    async def auth_send_key(self, user_id: int) -> AuthInfoEnum:
        client = self.get_client(user_id)
        if not client:
            return AuthInfoEnum.CLIENT_NOT_FOUND
        
        status = await client.connect()

        if status:
            await client.disconnect()
            return AuthInfoEnum.CLIENT_AUTH_SUCCSESS
        
        result = await client.send_code(client.phone_number)
        self.hash_code[user_id] = result.phone_code_hash
        
        return AuthInfoEnum.CLIENT_AUTH_SEND_CODE

    async def auth_code(self, user_id: int, code: str) -> AuthInfoEnum:
        client = self.get_client(user_id)
        if not client:
            return AuthInfoEnum.CLIENT_NOT_FOUND
        
        hash_code = self.get_hash_code(user_id)

        if not hash_code:
            return AuthInfoEnum.CLIENT_HASH_CODE_NOT_FOUND
        
        try:
            result = await client.sign_in(
                phone_number=client.phone_number,
                phone_code_hash=hash_code,
                phone_code=code
            )
        except errors.PhoneCodeExpired:
            return AuthInfoEnum.CLIENT_PHONE_CODE_EXPIRED
        except errors.SessionPasswordNeeded:
            try:
                result = await client.check_password(client.password)
            except errors.PasswordHashInvalid:
                return AuthInfoEnum.CLIENT_PASSWORD_INVALID
            except:
                return AuthInfoEnum.CLIENT_AUTH_WRONG
            
        await client.disconnect()

        return AuthInfoEnum.CLIENT_AUTH_SUCCSESS

    def get_status_client(self, user_id: int) -> bool:
        return self.client_running.get(user_id, False)

    async def pooling_server(self) -> None:
        async def any_command_handler(*args, **kwargs):
            ...
        commands = {
            TaskTypeEnum.EAT_FROG: handle_auto_eat_toad,
            TaskTypeEnum.EAT_TOAD: handle_auto_eat_baby_toad,
            TaskTypeEnum.REWARD_CLAN: handle_cmd_reward_clan,
            TaskTypeEnum.REWARD_MARRIAGE: handle_cmd_reward_marriage,
            TaskTypeEnum.FROG_DAY: handle_cmd_toad_day,
            TaskTypeEnum.WORK: handle_cmd_work,
        }
        any_command = any_command_handler
        while True:
            await asyncio_sleep(30)
            try:
                user_ids: list[int] = [
                    client_id for client_id, client in self.clients.items() 
                    if client.is_connected
                ]
                if not user_ids:
                    continue
                tasks = await config.WEB_API.get_ready_tasks(user_ids)
                for task in tasks:
                    coro = commands.get(task.task_type, any_command)
                    asyncio_create_task(coro, self.clients.get(task.user_id))
            except Exception as e:
                ...

AuthInfoClass = AuthInfo()
