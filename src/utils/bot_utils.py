import requests

from typing import Any, Dict


from constants.application import BACKEND_GET_BOT_INFO_PATH, BACKEND_HOST
from constants.bot_data_keys import *


def reset_bot_data(bot_data: Dict[str, Any]) -> None:
    bot_data[IS_ACTIVE] = False
    bot_data[QUESTIONS_COUNT] = 0
    bot_data[USERS_LAST_QUESTION_TIMESTAMP] = dict()

    backend_response = requests.get("".join([BACKEND_HOST, BACKEND_GET_BOT_INFO_PATH])).json()

    bot_data[AUTHENTICATED_USERS] = backend_response[AUTHENTICATED_USERS]
    bot_data[NEW_QUESTION_DURATION_LIMIT] = backend_response[NEW_QUESTION_DURATION_LIMIT]
    bot_data[NEW_QUESTION_CHARACTERS_LIMIT] = backend_response[NEW_QUESTION_CHARACTERS_LIMIT]

    bot_data[START_MESSAGE] = backend_response[START_MESSAGE]
    bot_data[DURUS_MESSAGE] = backend_response[DURUS_MESSAGE]
    bot_data[GROUPS_MESSAGE] = backend_response[GROUPS_MESSAGE]
