import time
import sys
import os
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib import discord_integration
from src.lib.embed import new_embed

description = """Look at information regarding this bot."""
start_time = time.time()

async def run(ctx, *args):
    #uptime
    current_time = time.time()
    uptime = start_time - current_time
    #guilds
    guild_count = len(ctx.bot.guilds)
    #ping
    ping = time.time() - ctx.message.created_at
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
    command_dir = "./"
    cmds = len(glob.glob(command_dir + "*.py"))
    #language the bot is coded in
    language = "Python"
    #Github Repo Link
    source_code = "https://github.com/kty990/HomieColab"
