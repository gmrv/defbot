import logging
from common import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, ChatPermissions
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)

app_config = config.get_config()

def chat_member(update: Update, context: CallbackContext) -> None:
    logger.info(update.message.new_chat_members[0].mention_markdown_v2())
    user_id = update.message.new_chat_members[0].id
    a = context.bot.restrict_chat_member(
        update.message.chat_id,
        user_id,
        ChatPermissions(can_send_messages=False)
    )
    logger.info(a)
    #update.message.reply_text(f"Привет, {update.message.new_chat_members[0].first_name}! Вам разрешено только чтение, для разрешения отправки сообщений свяжитесь с администраторами группы.")