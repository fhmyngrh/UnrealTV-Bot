'''
tg-stream-video, An Telegram Bot Project
Copyright (c) 2021 GalihMrd <https://github.com/Imszy17>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

import os
import pafy
import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
     InlineKeyboardButton,
     InlineKeyboardMarkup,
     Message,
)
from lib.config import USERNAME_BOT
from lib.tg_stream import group_call_factory
from lib.driver.misc import CHANNEL_VIDEO, VIDEO_CALL, PAUSE, RESUME
from lib.helpers.filters import private_filters, public_filters

group_call = group_call_factory.get_group_call()


@Client.on_message(filters.command(["ytstream",
                                    "ytstream@{USERNAME_BOT}"]) & public_filters)
async def ytstream(client, message):
    query = message.command[1]
    rby = message.from_user.mention
    chat_id = message.chat.id
    txt = await message.reply(f"```Converting url...```\nUrl: ```{query}```")
    try:
        video = pafy.new(query)
        title = video.title
        duration = video.duration
        final_source = video.getbest().url
    except Exception as e:
        await message.reply(f'**Error:** {e}')
    if len(message.command) < 2:
        await message.reply("Give some youtube video url")
    else:
        if not group_call.is_connected:
            await group_call.join(chat_id)
        else:
            await group_call.stop()
            await asyncio.sleep(3)
            await group_call.join(chat_id)
        await group_call.start_video(final_source, enable_experimental_lip_sync=True)
        VIDEO_CALL[chat_id] = group_call
        PAUSE[chat_id] = group_call
        RESUME[chat_id] = group_call
        await txt.delete()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        '📣 Channel support', url='https://t.me/feyystatus',
                    ),
                ],
            ],
        )
        await message.reply_photo(
            caption=f"**Streaming [{title}]({query})**\n**Duration:** {duration}\n**Requested by:** {rby}\n**To stop:** /stop",
            photo="./etc/banner.png",
            reply_markup=keyboard,
        )

@Client.on_message(filters.command(["ytcstream",
                                    "ytstream@{USERNAME_BOT}"]) & public_filters)
async def cstream(client, message):
    query = message.command[1]
    rby = message.from_user.mention
    chat_id = message.chat.title
    text = await message.reply(f"```Converting url...```\nUrl: ```{query}```")
    try:
        video = pafy.new(query)
        title = video.title
        duration = video.duration
        source = video.getbest().url
    except Exception as e:
        await message.reply(f'**Error:** {e}')
    if len(message.command) < 2:
        await message.reply("Give some youtube url")
    else:
        if not group_call.is_connected:
            await group_call.join(int(chat_id))
        else:
            await group_call.stop()
            await asyncio.sleep(3)
            await group_call.join(int(chat_id))
        await group_call.start_video(source, enable_experimental_lip_sync=True)
        CHANNEL_VIDEO[chat_id] = group_call
        await text.delete()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        '📣 Channel support', url='https://t.me/feyystatus',
                    ),
                ],
            ],
        )
        await message.reply_photo(
            caption=f"**Streaming [{title}]({query})**\n**Duration:** {duration}\n**Requested by:** {rby}\n**To stop:** /cstop",
            photo="./etc/banner.png",
            reply_markup=keyboard,
        )

@group_call.on_playout_ended
async def media_ended(gc, source, media_type):
    print(f'{media_type} ended: {source}')
    try:
        await group_call.stop()
        os.remove(source)
    except Exception:
        pass
