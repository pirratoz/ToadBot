import re

from pyrogram.client import Client
from pyrogram.types import Message



class Patten:
    pattern1 = re.compile(r"(\d+.*) =", re.MULTILINE)
    pattern2 = lambda result_eval: re.compile(f"(\d)\) {result_eval}")


async def handle_calculate_expression(client: Client, message: Message) -> None:
    condition = re.findall(Patten.pattern1, message.text)[0]

    result_eval = eval(condition)

    answer = re.findall(Patten.pattern2(result_eval), message.text)[0]

    icons = {
        "0": "0️⃣",
        "1": "1️⃣",
        "2": "2️⃣",
        "3": "3️⃣",
        "4": "4️⃣",
        "5": "5️⃣",
        "6": "6️⃣",
        "7": "7️⃣",
        "8": "8️⃣",
        "9": "9️⃣",
    }
    await client.send_message(
        message.chat.id,
        text=f"{icons[answer]} | {condition} = {result_eval}"
    )
