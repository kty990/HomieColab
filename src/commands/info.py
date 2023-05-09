import time
import sys
import os
import glob
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib import discord_integration
from src.lib.embed import new_embed

description = """Look at information regarding this bot."""
start_time = time.time()

print(os.getcwd())

def convertToFormat(s):
    seconds = s
    minutes = math.floor(seconds/60)
    hours = math.floor(minutes/60)
    minutes -= (hours*60)
    seconds -= (minutes*60)
    return f"{f'{hours}h:' if hours > 0 else ''}{f'{minutes}m:' if minutes > 9 else f'0{minutes}m:'}{f'{seconds}s' if seconds > 9 else f'0{seconds}s'}"

async def run(ctx, *args):
    #uptime
    current_time = time.time()
    uptime = round(abs(start_time - current_time),2)
    #guilds
    guild_count = len(ctx.bot.guilds)
    #ping
    ping = round(abs(time.time() - ctx.message.created_at.timestamp()),2)
    #name
    name = str(ctx.bot.user)
    #ID
    id = ctx.bot.user.id
    #owners
    owners = "kty990#2023"
    #prefix
    prefix = '-'
    #user count
    users = sum([guild.member_count for guild in ctx.bot.guilds])
    #version
    version = "0.8.9"
    #number of commands
    command_dir = "./src/commands/"
    cmds = len(glob.glob(command_dir + "*.py"))
    #language the bot is coded in
    language = "Python"
    #Github Repo Link
    source_code = "https://github.com/kty990/HomieColab"
    prompt_list = [
        f"**Uptime:** {convertToFormat(uptime)}",
        f"**Guilds:** {guild_count}",
        f"**Ping:** {convertToFormat(ping)}",
        f"**Name:** {name}",
        f"**ID:** {id}",
        f"**Owners:** {owners}",
        f"**Prefix:** {prefix}",
        f"**Users:** {users}",
        f"**Version:** {version}",
        f"**Commands:** {cmds}",
        f"**Language:** {language}",
        f"**Source:** {source_code}"
    ]
    prompt_list.sort()
    e = new_embed("Bot Info","\n".join(prompt_list))
    await discord_integration.send_message(ctx,None,e)
