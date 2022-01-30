from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from constants.bot_data_keys import IS_ACTIVE
from utils.bot_utils import reset_bot_data

from utils.handler_utils import (
    send_bot_activated_message,
    send_received_questions_message,
    send_bot_deactivated_message,
)


def toggle(update: Update, context: CallbackContext) -> None:
    if context.bot_data[IS_ACTIVE]:
        deactivate(update, context)
    else:
        activate(update, context)


def activate(update: Update, context: CallbackContext) -> None:
    context.bot_data[IS_ACTIVE] = True
    send_bot_activated_message(update, context)


def deactivate(update: Update, context: CallbackContext) -> None:
    send_received_questions_message(update, context)
    reset_bot_data(context.bot_data)
    send_bot_deactivated_message(update, context)
