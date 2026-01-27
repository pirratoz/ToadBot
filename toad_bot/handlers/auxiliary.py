from pyrogram import filters
from pyrogram.handlers import MessageHandler

from toad_bot.commands.calculator import handle_calculate_expression
from toad_bot.commands.hiking import handle_hiking_click_button
from toad_bot.commands.casino import handle_casino_click_button

from toad_bot.storage.config import TOAD_BOT_ID
import toad_bot.filters as f


def get_auxiliary_handlers():
    return [
        MessageHandler(
            handle_calculate_expression,
            filters=filters.regex(r"Осматривая все служебные помещения, вы находите защищенную комнату охраны.")
        ),
        MessageHandler(
            handle_hiking_click_button,
            filters=filters.regex(r"Сейчас выбирает ход") & filters.user(TOAD_BOT_ID) & f.check_mention()
        ),
        MessageHandler(
            handle_casino_click_button,
            filters=filters.regex(r"Твой стол готов! 🎰") & filters.user(TOAD_BOT_ID) & f.check_mention()
        ),
    ]