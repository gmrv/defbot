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
    logger.debug(f"NEW_CHAT_MEMBERS: {update.message.new_chat_members[0].mention_markdown_v2()}")

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

def left_chat_member(update: Update, context: CallbackContext) -> None:
    logger.debug(f"LEFT_CHAT_MEMBER: {update}")


def chat_member_change(update:Update, context: CallbackContext) -> None:
    logger.debug(f"CHAT_MEMBER_CHANGE: {update}")


def antispam(update, context):
    logger.debug(f"ANTISPAM: {update}")
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
        message_has_links = utils.is_contains_stop_words(text, app_config.STOP_WORDS)
        logger.info(
            f"User {user_id} joined the chat ({chat_id}) on {join_date.strftime('%Y-%m-%d %H:%M:%S')}, time_difference={time_difference}, is_less_one_day={is_less_one_day}, message_has_links={message_has_links}")
        if (is_less_one_day and message_has_links):
            context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            logger.info("Message removed successfully.")
            #context.bot.send_message(chat_id=chat_id, text=f"@{username} новым пользователям запрещено постить ссылки.")
    else:
        logger.info(f"Join date of user {user_id} is not known yet. It may have joined before the bot started logging.")


def message_handler(update, context):
    logger.debug(f"MESSAGE_HANDLER: {update}")

    # Handle command
    if update.message.text[0] == ".":
        # if sender is not the owner do nothing
            is_success = command_handler(update, context)
            if is_success: return
    # Handle message
    if not app_config.IS_ANTISPAM_ACTIVE:
        logger.debug(f"ANTISPAM_SIMPLE: Antispam not active")
        return
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text.replace('\n', '').replace('\r', '')
    logger.info(text)
    if utils.is_contains_stop_words(text, app_config.STOP_WORDS) or utils.has_alphanumeric_words(text):
        update.message.reply_text(f"Сообщение удалено. Подозрение на спам.")
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        logger.info("Message removed successfully.")
        # context.bot.send_message(chat_id=chat_id, text=f"Сообщение удалено. Подозрение на спам.")


def all_over(update: Update, context: CallbackContext) -> None:
    logger.debug(f"ALL_OVER: {update}")

def command_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not user_id == int(app_config.MASTER_ID): return False
    command = update.message.text.split()
    logger.debug(f"COMMAND: {command}")
    if command[0] == ".+":
        lst = str.join(' ', command[1:]).split(', ')
        logger.debug(f"add words to file: {lst}" )
        utils.append_list_to_file(app_config.STOP_WORDS_FILE, lst)
        app_config.update()
        update.message.reply_text(f"{app_config.STOP_WORDS}")
        logger.info(f"STOP WORDS: {app_config.STOP_WORDS}")
        return True
    if command[0] == ".-":
        lst_to_remove = str.join(' ', command[1:]).split(', ')
        result_list = utils.remove_elements(app_config.STOP_WORDS, lst_to_remove)
        logger.debug(f"remove words: {lst_to_remove}" )
        utils.write_list_to_file(app_config.STOP_WORDS_FILE, result_list)
        app_config.update()
        update.message.reply_text(f"{app_config.STOP_WORDS}")
        logger.info(f"STOP WORDS: {app_config.STOP_WORDS}")
        return True
    elif command[0] == ".a0":
        app_config.IS_ANTISPAM_ACTIVE = False
        logger.info("Now antispam inactive")
        update.message.reply_text(f"Now antispam inactive")
        return True
    elif command[0] == ".a1":
        app_config.IS_ANTISPAM_ACTIVE = True
        logger.info("Now antispam active")
        update.message.reply_text(f"Now antispam active")
        return True
    elif command[0] == ".ls":
        update.message.reply_text(f"{app_config.STOP_WORDS}")
        return True
    else:
        return False
