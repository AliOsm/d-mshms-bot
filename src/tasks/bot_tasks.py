import datetime

from typing import Callable, Dict, Union

import pytz

from telegram.constants import PARSEMODE_MARKDOWN_V2
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.jobqueue import JobQueue

from constants.application import DURUS_GROUP_ID


def create_drs_reminder_callback(text: str) -> Callable[[CallbackContext], None]:
    return lambda context: context.bot.send_message(
        chat_id=DURUS_GROUP_ID,
        text=text,
        parse_mode=PARSEMODE_MARKDOWN_V2,
        disable_web_page_preview=True,
    )


def create_drs_reminder_job(job_queue: JobQueue, drs_task: Dict[str, Union[str, int]]) -> None:
    job_queue.run_daily(
        callback=create_drs_reminder_callback(drs_task.text),
        time=datetime.time(
            hour=drs_task.hour,
            minute=drs_task.minute,
            tzinfo=pytz.timezone("Asia/Riyadh"),
        ),
        days=(drs_task.day,),
        name=drs_task.name,
    )
