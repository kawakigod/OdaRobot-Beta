# Copyright (C) 2021 Red-Aura & TeamDaisyX & HamkerCat

# This file is part of Daisy (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from asyncio import gather, sleep

from pyrogram import filters
from pyrogram.types import Message

from wbb import (BOT_ID, OWNER_ID, pbot, arq)
from wbb.utils.errors import capture_err
from wbb.utils.filter_groups import chatbot_group

daisy_chats = []
en_chats = []
# AI Chat (C) 2020-2021 by @RxyMX

async def chat_bot_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "enable":
        if chat_id not in db:
            db.append(chat_id)
            text = "Chatbot Enabled!"
            return await edit_or_reply(message, text=text)
        await edit_or_reply(
            message, text="ChatBot Is Already Enabled."
        )
    elif status == "disable":
        if chat_id in db:
            db.remove(chat_id)
            return await edit_or_reply(
                message, text="Chatbot Disabled!"
            )
        await edit_or_reply(
            message, text="ChatBot Is Already Disabled."
        )
    else:
        await edit_or_reply(
            message, text="**Usage**\n/chatbot [ENABLE|DISABLE]"
        )


# Enabled | Disable Chatbot


@pbot.on_message(filters.command("chatbot") & ~filters.edited)
@capture_err
async def chatbot_status(_, message: Message):
    if len(message.command) != 2:
        return await edit_or_reply(
            message, text="**Usage**\n/chatbot [ENABLE|DISABLE]"
        )
    await chat_bot_toggle(active_chats_bot, message)


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


async def type_and_send(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(3))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")


@pbot.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded,
    group=chatbot_group,
)
@capture_err
async def chatbot_talk(_, message: Message):
    if message.chat.id not in active_chats_bot:
        return
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    await type_and_send(message)



