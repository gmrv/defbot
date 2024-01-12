import logging
from common import config
from handlers import commands
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ChatMemberHandler, MessageHandler, Filters


config = config.get_config()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(config.TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, commands.chat_member))

    logger.info("Defbot started")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
