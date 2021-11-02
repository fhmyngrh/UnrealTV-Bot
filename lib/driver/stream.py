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

import asyncio
import os

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from lib.config import USERNAME_BOT
from lib.driver.misc import PAUSE, RESUME, VIDEO_CALL
from lib.helpers.filters import public_filters
from lib.tg_stream import group_call_factory

group_call = group_call_factory.get_group_call()


@Client.on_message(filters.command(["stream",
                                    "stream@{USERNAME_BOT}"]) & public_filters)
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("`Reply to some Video or Give Some Live Stream Url!`")
        else:
            livelink = m.text.split(None, 1)[1]
            msg = await m.reply("`Starting Live Stream...`")
            chat_id = m.chat.id
            user = m.from_user.mention
            await asyncio.sleep(1)
            try:
                if not group_call.is_connected:
                    await group_call.join(chat_id)
                else:
                    await group_call.stop()
                    await asyncio.sleep(3)
                    await group_call.join(chat_id)
                await group_call.start_video(livelink, repeat=False)
                VIDEO_CALL[chat_id] = group_call
                PAUSE[chat_id] = group_call
                RESUME[chat_id] = group_call
                await msg.delete()
                keyboard = InlineKeyboardMarkup(

                    [
                        [
                            InlineKeyboardButton(
                                'OWNER', url='https://t.me/UnrealZelda',
                            ),
                        ],
                    ],
                )
                await m.reply_photo(
                    photo="./etc/banner.png",
                    caption=f"**Started [Live Streaming](livelink) !**\n**Request by:** {user}\n**To stop:** /stop",
                    reply_markup=keyboard,
                )

            except Exception as e:
                await msg.edit(f"**Error** -- `{e}`")
    elif replied.video or replied.document:
        msg = await m.reply("`Downloading...`")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.id
        user = m.from_user.mention
        await asyncio.sleep(2)
        try:
            if not group_call.is_connected:
                await group_call.join(chat_id)
            else:
                await group_call.stop()
                await asyncio.sleep(3)
                await group_call.join(chat_id)
            await group_call.start_video(video, enable_experimental_lip_sync=True, repeat=False)
            VIDEO_CALL[chat_id] = group_call
            PAUSE[chat_id] = group_call
            RESUME[chat_id] = group_call
            await msg.delete()
            keyboard = InlineKeyboardMarkup(

                [
                    [
                        InlineKeyboardButton(
                            'OWNER', url='https://t.me/UnrealZelda',
                        ),
                    ],
                ],
            )
            await m.reply_photo(
                photo="./etc/banner.png",
                caption=f"**Streamed video from telegram files**\n**Requested by:** {user}\n**To stop:** /stop",
                reply_markup=keyboard,
            )
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("`Reply to some Video!`")


@Client.on_message(filters.command(["cstream",
                                    "cstream@{USERNAME_BOT}"]) & public_filters)
async def cstream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("`Reply to some Video or Give Some Live Stream Url!`")
        else:
            livelink = m.text.split(None, 1)[1]
            msg = await m.reply("`Starting Live Stream...`")
            chat_id = m.chat.title
            user = m.from_user.mention
            await asyncio.sleep(1)
            try:
                if not group_call.is_connected:
                    await group_call.join(int(chat_id))
                else:
                    await group_call.stop()
                    await asyncio.sleep(3)
                    await group_call.join(int(chat_id))
                await group_call.start_video(livelink, repeat=False)
                VIDEO_CALL[chat_id] = group_call
                PAUSE[chat_id] = group_call
                RESUME[chat_id] = group_call
                await msg.delete()
                keyboard = InlineKeyboardMarkup(

                    [
                        [
                            InlineKeyboardButton(
                                'OWNER', url='https://t.me/UnrealZelda',
                            ),
                        ],
                    ],
                )
                await m.reply_photo(
                    photo="./etc/banner.png",
                    caption=f"**Started [Live Streaming](livelink) !**\n**Request by:** {user}\n**To stop:** /stop",
                    reply_markup=keyboard,
                )

            except Exception as e:
                await msg.edit(f"**Error** -- `{e}`")
    elif replied.video or replied.document:
        msg = await m.reply("`Downloading...`")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.title
        user = m.from_user.mention
        await asyncio.sleep(2)
        try:
            if not group_call.is_connected:
                await group_call.join(int(chat_id))
            else:
                await group_call.stop()
                await asyncio.sleep(3)
                await group_call.join(int(chat_id))
            await group_call.start_video(video, enable_experimental_lip_sync=True, repeat=False)
            VIDEO_CALL[chat_id] = group_call
            PAUSE[chat_id] = group_call
            RESUME[chat_id] = group_call
            await msg.delete()
            keyboard = InlineKeyboardMarkup(

                [
                    [
                        InlineKeyboardButton(
                            'OWNER', url='https://t.me/UnrealZelda',
                        ),
                    ],
                ],
            )
            await m.reply_photo(
                photo="./etc/banner.png",
                caption=f"**Streamed video from telegram files**\n**Requested by:** {user}\n**To stop:** /cstop",
                reply_markup=keyboard,
            )
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("`Reply to some Video!`")


@group_call.on_playout_ended
async def media_ended(gc, source, media_type):
    print(f'{media_type} ended: {source}')
    try:
        await group_call.stop()
        os.remove(source)
    except Exception:
        pass
