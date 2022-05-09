import os
import asyncio
import time
from datetime import datetime

import psutil

from handlers import StartTime
from helpers.filters import command
from telegram.utils.helpers import escape_markdown, mention_html
from config import BOT_USERNAME, SUPPORT_GROUP, PING_IMG, BOT_NAME
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


@Client.on_message(command(["vcping"]) & filters.group & ~filters.edited & ~filters.private)

async def help(client: Client, message: Message):
    await message.delete()
    boottime = time.time()
    bot_uptime = escape_markdown(get_readable_time((time.time() - StartTime)))
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    start = datetime.now()
    resp = (datetime.now() - start).microseconds / 1000
    await message.reply_sticker("CAACAgUAAx0CXJU7zQABCEDkYnk5pTbx5HvEbd3trrY2rc66j_IAArYCAAJ8vfFUbqGdrKTeHgwkBA")
    rahul = await message.reply_photo(
        photo=f"{PING_IMG}",
        caption="Pong...",
    )
    await rahul.edit_text(
        f"""<b> Pong ! </b>\n  🏓 `{resp} ms`\n\n<b><u>{BOT_NAME} sʏsᴛᴇᴍ sᴛᴀᴛs:</u></b>\n\n• Uptime : {bot_uptime}\n• CPU : {cpu}%\n• Disk : {disk}%\n• RAM : {mem}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Support", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                ]
            ]
        ),
    )
