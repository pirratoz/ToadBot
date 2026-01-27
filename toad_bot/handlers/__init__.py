__all__ = [
    "init_handlers",
]


from pyrogram.client import Client

from toad_bot.handlers.auxiliary import get_auxiliary_handlers


def init_handlers(client: Client) -> None:
    handlers = [
        *get_auxiliary_handlers()
    ]
    for handler in handlers:
        client.add_handler(handler)
