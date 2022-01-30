import os
import datetime

from typing import Dict, List, Union

from prodict import Prodict
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.jobqueue import JobQueue

from constants.application import BOT_HOST
from constants.bot_data_keys import AUTHENTICATED_USERS
from handlers.auth_user_handlers import toggle
from handlers.normal_user_handlers import start, durus, groups, status, text_handler, error_handler
from tasks.bot_tasks import create_drs_reminder_job
from tasks.server_tasks import ping_bot_and_backend_host
from utils.bot_utils import reset_bot_data
from utils.file_utils import read_json


def add_tasks(job_queue: JobQueue) -> None:
    job_queue.run_repeating(ping_bot_and_backend_host, interval=datetime.timedelta(minutes=5))

    weekly_durus_tasks: List[Dict[str, Union[str, int]]] = read_json("data/weekly_durus_tasks.json")
    for drs_task in weekly_durus_tasks:
        create_drs_reminder_job(job_queue, Prodict.from_dict(drs_task))


def add_handlers(dispatcher: Dispatcher) -> None:
    for handler_name, handler_callback, filters in [
        ("start", start, None),
        ("durus", durus, None),
        ("groups", groups, None),
        ("status", status, None),
        ("toggle", toggle, Filters.user(username=dispatcher.bot_data[AUTHENTICATED_USERS].split(","))),
    ]:
        dispatcher.add_handler(CommandHandler(handler_name, handler_callback, filters))

    dispatcher.add_handler(MessageHandler(~Filters.command & ~Filters.chat_type.groups & Filters.text, text_handler))

    dispatcher.add_error_handler(error_handler)


def main() -> None:
    updater: Updater = Updater(os.environ["BOT_TOKEN"])
    job_queue: JobQueue = updater.job_queue
    dispatcher: Dispatcher = updater.dispatcher

    reset_bot_data(dispatcher.bot_data)

    add_tasks(job_queue)
    add_handlers(dispatcher)

    updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=os.environ["BOT_TOKEN"],
        webhook_url="/".join([BOT_HOST, os.environ["BOT_TOKEN"]]),
    )

    updater.idle()


if __name__ == "__main__":
    main()
