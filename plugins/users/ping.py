import os

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("pingad", "!"))
async def ping(c: Client, m: Message):
    screen = os.environ.get("STY", "")

    await m.reply_text("Pong! " + screen)
