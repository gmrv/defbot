import logging
from logging.handlers import RotatingFileHandler

from common import config
from handlers import commands
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ChatMemberHandler, MessageHandler, Filters

config = config.get_config()

# Enable logging
logging.basicConfig(
    filename="./logs/defbot.log", filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=config.TRACE_LEVEL
)
logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(config.TOKEN)
    dispatcher = updater.dispatcher

    if config.IS_ANTISPAM_ACTIVE:
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, commands.antispam_simple))

    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, commands.new_chat_member))
    dispatcher.add_handler(MessageHandler(None, commands.all_over))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, commands.left_chat_member))
    dispatcher.add_handler(ChatMemberHandler(commands.chat_member_change, None))

    logger.info("Defbot started")
    logger.debug(f"Stop words: {config.STOP_WORDS}")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
