import logging
from logging.handlers import RotatingFileHandler

from common import config, utils
from handlers import commands
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ChatMemberHandler, MessageHandler, Filters

app_config = config.get_config()

# Enable logging
logging.basicConfig(
    filename="./logs/defbot.log", filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=app_config.TRACE_LEVEL
)
logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(app_config.TOKEN)
    app_config.set_updater(updater)

    dispatcher = updater.dispatcher

    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, commands.message_handler))
    dispatcher.add_handler(MessageHandler(None, commands.message_handler))

    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, commands.new_chat_member))
    dispatcher.add_handler(MessageHandler(None, commands.all_over))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, commands.left_chat_member))
    dispatcher.add_handler(ChatMemberHandler(commands.chat_member_change, None))

    logger.info("Defbot started")
    utils.send_log_chat("Defbot started")
    logger.debug(f"Stop words: {app_config.STOP_WORDS}")
    logger.debug(f"Trusted users id: {app_config.TRUSTED_ID}")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
