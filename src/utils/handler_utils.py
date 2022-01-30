from typing import List, Union

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from thefuzz import fuzz

from constants.application import BACKUP_GROUP_ID, MINIMUM_TOKENS, QUESTIONS_GROUP_ID, SIMILARITY_THRESHOLD

from constants.bot_data_keys import (
    NEW_QUESTION_CHARACTERS_LIMIT,
    NEW_QUESTION_DURATION_LIMIT,
    QUESTIONS_COUNT,
    SESSION_QUESTIONS,
    USERS_LAST_QUESTION_TIMESTAMP,
)

from constants.messages import (
    BOT_ACTIVATED_SUCCESSFULLY,
    BOT_DEACTIVATED_SUCCESSFULLY,
    NEW_QUESTION_CHARACTERS_LIMIT_TEMPLATE,
    NEW_QUESTION_DURATION_LIMIT_TEMPLATE,
    NO_ENOUGH_INFORMATION,
    QUESTION_RECEIVED_TEMPLATE,
    RECEIVED_QUESTIONS_TEMPLATE,
    REDIRECT_QUESTION_TEMPLATE,
    SIMILAR_QUESTION_RECEIVED,
)


def send_message_to_groups(context: CallbackContext, text: str) -> None:
    for group in [QUESTIONS_GROUP_ID, BACKUP_GROUP_ID]:
        context.bot.send_message(chat_id=group, text=text)


def confirm_and_redirect_received_question_to_questions_group(update: Update, context: CallbackContext) -> None:
    context.bot_data[QUESTIONS_COUNT] += 1
    context.bot_data[SESSION_QUESTIONS].append(update.message.text)

    update.message.reply_text(text=QUESTION_RECEIVED_TEMPLATE.format(context.bot_data[QUESTIONS_COUNT]))
    send_message_to_groups(
        context,
        REDIRECT_QUESTION_TEMPLATE.format(context.bot_data[QUESTIONS_COUNT], update.message.text),
    )


def send_bot_activated_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text=BOT_ACTIVATED_SUCCESSFULLY)
    send_message_to_groups(context, BOT_ACTIVATED_SUCCESSFULLY)


def send_received_questions_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text=RECEIVED_QUESTIONS_TEMPLATE.format(context.bot_data[QUESTIONS_COUNT]))
    send_message_to_groups(context, RECEIVED_QUESTIONS_TEMPLATE.format(context.bot_data[QUESTIONS_COUNT]))


def send_bot_deactivated_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text=BOT_DEACTIVATED_SUCCESSFULLY)
    send_message_to_groups(context, BOT_DEACTIVATED_SUCCESSFULLY)


def get_user_last_question_difference(update: Update, context: CallbackContext) -> int:
    user_last_message_timestamp = context.bot_data[USERS_LAST_QUESTION_TIMESTAMP][update.message.from_user.username]
    return (update.message.date - user_last_message_timestamp).total_seconds()


def can_user_send_question(update: Update, context: CallbackContext) -> bool:
    if update.message.from_user.username in context.bot_data[USERS_LAST_QUESTION_TIMESTAMP]:
        return get_user_last_question_difference(update, context) > context.bot_data[NEW_QUESTION_DURATION_LIMIT]
    return True


def calculate_new_question_similarity_with_session_questions(new_question: str, session_questions: List[str]) -> float:
    return max([0] + [fuzz.ratio(question, new_question) for question in session_questions])


def validate_message_and_get_reply_text(update: Update, context: CallbackContext) -> Union[None, str]:
    if len(update.message.text.split()) < MINIMUM_TOKENS:
        return NO_ENOUGH_INFORMATION
    elif len(update.message.text) > context.bot_data[NEW_QUESTION_CHARACTERS_LIMIT]:
        return NEW_QUESTION_CHARACTERS_LIMIT_TEMPLATE.format(
            len(update.message.text),
            context.bot_data[NEW_QUESTION_CHARACTERS_LIMIT],
        )
    elif not can_user_send_question(update, context):
        return NEW_QUESTION_DURATION_LIMIT_TEMPLATE.format(
            int(context.bot_data[NEW_QUESTION_DURATION_LIMIT] - get_user_last_question_difference(update, context)),
        )
    elif (
        calculate_new_question_similarity_with_session_questions(
            update.message.text,
            context.bot_data[SESSION_QUESTIONS],
        )
        > SIMILARITY_THRESHOLD
    ):
        return SIMILAR_QUESTION_RECEIVED

    return None
