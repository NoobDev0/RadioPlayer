"""
RadioPlayer, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

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
"""

import os
import sys
import asyncio
import subprocess
from threading import Thread
from signal import SIGINT
from pyrogram import Client, filters, idle
from config import Config
from utils import mp, USERNAME, FFMPEG_PROCESSES
from pyrogram.raw import functions, types

CHAT=Config.CHAT
ADMINS=Config.ADMINS

bot = Client(
    "RadioPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
async def main():
    async with bot:
        await mp.start_radio()

def stop_and_restart():
    bot.stop()
    os.system("git pull")
    os.execl(sys.executable, sys.executable, *sys.argv)


bot.run(main())
bot.start()
print("\n\nRadio Player Bot Started, Join @Cinema_Haunter")
bot.send(
    functions.bots.SetBotCommands(
        commands=[
            types.BotCommand(
                command="start",
                description="Start The Bot"
            ),
            types.BotCommand(
                command="help",
                description="Show Help Message"
            ),
            types.BotCommand(
                command="play",
                description="Play Song From YouTube"
            ),
            types.BotCommand(
                command="song",
                description="Download Song As Audio"
            ),
            types.BotCommand(
                command="pause",
                description="Pause The Current Song"
            ),
            types.BotCommand(
                command="resume",
                description="Resume The Paused Song"
            ),
            types.BotCommand(
                command="radio",
                description="Start Radio / Live Stream"
            ),
            types.BotCommand(
                command="stopradio",
                description="Stop Radio / Live Stream"
            ),
            types.BotCommand(
                command="current",
                description="Show Current Playing Song"
            ),
            types.BotCommand(
                command="playlist",
                description="Show The Current Playlist"
            ),
            types.BotCommand(
                command="volume",
                description="Change Voice Chat Volume"
            ),
            types.BotCommand(
                command="skip",
                description="Skip The Current Song"
            ),
            types.BotCommand(
                command="join",
                description="Join To The Voice Chat"
            ),
            types.BotCommand(
                command="leave",
                description="Leave From The Voice Chat"
            ),
            types.BotCommand(
                command="stop",
                description="Stop Playing The Music"
            ),
            types.BotCommand(
                command="replay",
                description="Replay From The Begining"
            ),
            types.BotCommand(
                command="clean",
                description="Clean Unused RAW PCM Files"
            ),
            types.BotCommand(
                command="mute",
                description="Mute Userbot In Voice Chat"
            ),
            types.BotCommand(
                command="unmute",
                description="Unmute Userbot In Voice Chat"
            ),
            types.BotCommand(
                command="update",
                description="Update Your Bot (Owner Only)"
            ),
            types.BotCommand(
                command="restart",
                description="Restart Your Bot (Owner Only)"
            )
        ]
    )
)

@bot.on_message(filters.command(["update", f"update@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT) | filters.private))
async def updater(client, message):
    k=await message.reply_text("🔄 **Updating, Please Wait...**")
    await asyncio.sleep(3)
    await k.edit("🔄 **Successfully Updated. \nNow Restarting ...**")
    try:
        await message.delete()
    except:
        pass
    process = FFMPEG_PROCESSES.get(CHAT)
    if process:
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(e)
            pass
        FFMPEG_PROCESSES[CHAT] = ""
    Thread(
        target=stop_and_restart
        ).start()    


idle()
bot.stop()
print("\n\nRadio Player Bot Stopped, Join @AsmSafone!")
