import requests

from constants.application import BOT_HOST


def ping_bot_host(_) -> None:
    requests.get(BOT_HOST)
