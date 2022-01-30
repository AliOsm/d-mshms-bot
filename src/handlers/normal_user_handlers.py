import logging

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from constants.bot_data_keys import (
    DURUS_MESSAGE,
    GROUPS_MESSAGE,
    IS_ACTIVE,
    START_MESSAGE,
    USERS_LAST_QUESTION_TIMESTAMP,
)

from constants.messages import (
    BOT_IS_ACTIVATED_STATUS,
    BOT_IS_DEACTIVATED_STATUS,
    BOT_IS_DEACTIVATED,
)

from utils.handler_utils import (
    confirm_and_redirect_received_question_to_questions_group,
    validate_message_and_get_reply_text,
)


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text=context.bot_data[START_MESSAGE])


def durus(update: Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(text=context.bot_data[DURUS_MESSAGE], disable_web_page_preview=True)


def groups(update: Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(text=context.bot_data[GROUPS_MESSAGE], disable_web_page_preview=True)


def status(update: Update, context: CallbackContext) -> None:
    if context.bot_data[IS_ACTIVE]:
        update.message.reply_text(text=BOT_IS_ACTIVATED_STATUS)
    else:
        update.message.reply_text(text=BOT_IS_DEACTIVATED_STATUS)


def activated_bot_text_handler(update: Update, context: CallbackContext) -> None:
    reply_text = validate_message_and_get_reply_text(update, context)

    if reply_text:
        update.message.reply_text(text=reply_text)
    else:
        context.bot_data[USERS_LAST_QUESTION_TIMESTAMP][update.message.from_user.username] = update.message.date
        confirm_and_redirect_received_question_to_questions_group(update, context)


def text_handler(update: Update, context: CallbackContext) -> None:
    if context.bot_data[IS_ACTIVE]:
        activated_bot_text_handler(update, context)
    else:
        update.message.reply_text(text=BOT_IS_DEACTIVATED)


def error_handler(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s".', update, context.error)
