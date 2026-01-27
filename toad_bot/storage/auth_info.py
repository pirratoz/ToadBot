from pathlib import Path
from os import (
    getenv,
    makedirs,
    path
)


from pyrogram import (
    Client,
    errors,
)

from toad_bot.enums import AuthInfoEnum
from toad_bot.storage import config
from toad_bot.handlers import init_handlers


class AuthInfo:
    def __init__(self):
        self.clients: dict[int, Client] = {}
        self.hash_code: dict[int, str] = {}
    
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
        return client
    
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

AuthInfoClass = AuthInfo()
