import asyncio
from os import getenv

from dotenv import load_dotenv

from toad_bot.storage import AuthInfoClass
from toad_bot.enums import AuthInfoEnum


async def main() -> None:
    load_dotenv()
    user_id = int(getenv("TG_USER_ID"))
    api_id = getenv("TG_API_ID")
    api_hash = getenv("TG_API_HASH")
    password_2fa = getenv("TG_PASSWORD_2FA")
    phone = getenv("TG_PHONE")
    client = AuthInfoClass.add_client(
        user_id=user_id,
        api_id=api_id,
        api_hash=api_hash,
        password_2fa=password_2fa,
        phone=phone
    )
    result = await AuthInfoClass.is_auth(user_id)
    if not result == AuthInfoEnum.CLIENT_AUTH_SUCCSESS:
        result = await AuthInfoClass.auth_send_key(user_id)
        result = await AuthInfoClass.auth_code(user_id, code=input("[code] = "))
    
    status = await client.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
