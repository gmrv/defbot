import logging
import pytz
from common import config, utils
from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

app_config = config.get_config()

user_join_dates = {}


def new_chat_member(update: Update, context: CallbackContext) -> None:
    logger.info(update.message.new_chat_members[0].mention_markdown_v2())

    new_members = update.message.new_chat_members
    chat_id = update.message.chat_id

    for member in new_members:
        user_id = member.id
        join_date = datetime.now(app_config.TZ)
        user_join_dates[user_id] = join_date
        logger.info(f"User {member.username}({user_id}) joined the chat on {join_date.strftime('%Y-%m-%d %H:%M:%S')}")
    # Restrict user
    # user_id = update.message.new_chat_members[0].id
    # a = context.bot.restrict_chat_member(
    #     update.message.chat_id,
    #     user_id,
    #     ChatPermissions(can_send_messages=False)
    # )
    # logger.info(a)
    # update.message.reply_text(f"Привет, {update.message.new_chat_members[0].first_name}! Вам разрешено только чтение, для разрешения отправки сообщений свяжитесь с администраторами группы.")


def antispam(update, context):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text.replace('\n', '').replace('\r', '')
    logger.info(text)

    # Check if the user's join date is already known
    if user_id in user_join_dates:
        join_date = user_join_dates[user_id]
        current_time = datetime.now(app_config.TZ)
        time_difference = current_time - join_date
        is_less_one_day = abs(time_difference) <= timedelta(days=1)
        message_has_links = utils.has_links(text)
        logger.info(
            f"User {user_id} joined the chat ({chat_id}) on {join_date.strftime('%Y-%m-%d %H:%M:%S')}, time_difference={time_difference}, is_less_one_day={is_less_one_day}, message_has_links={message_has_links}")
        if (is_less_one_day and message_has_links):
            context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            logger.info("Message removed successfully.")
            context.bot.send_message(chat_id=chat_id, text=f"@{username} новым пользователям запрещено постить ссылки.")
    else:
        logger.info(f"Join date of user {user_id} is not known yet. It may have joined before the bot started logging.")


def antispam_simple(update, context):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text.replace('\n', '').replace('\r', '')
    logger.info(text)
    if utils.message_has_links(text):
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        logger.info("Message removed successfully.")
        context.bot.send_message(chat_id=chat_id, text=f"@{username} Размещение ссылок временно запрещено.")

def all_over(update: Update, context: CallbackContext) -> None:
    logger.debug(f"ALL_OVER update = {update}");