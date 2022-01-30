import requests

from constants.application import BACKEND_HOST, BOT_HOST


def ping_bot_and_backend_host(_) -> None:
    requests.get(BOT_HOST)
    requests.get(BACKEND_HOST)
