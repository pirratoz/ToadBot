from pyrogram import filters
from pyrogram.handlers import MessageHandler

from toad_bot.commands.calculator import handle_calculate_expression
from toad_bot.commands.auto_reward_marriage import handle_cmd_reward_marriage
from toad_bot.commands.auto_reward_clan import handle_cmd_reward_clan
from toad_bot.commands.auto_hiking import handle_hiking_click_button
from toad_bot.commands.auto_eat_toad import handle_auto_eat_toad
from toad_bot.commands.auto_eat_baby_toad import handle_auto_eat_baby_toad

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

    ]