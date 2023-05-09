import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import discord_integration
from src.lib.embed import new_embed
from src.lib.util import remove_files_by_pattern

description = "Dev only command."

def error(txt):
    e = new_embed("Error!",str(txt or "An unknown error occured"),0xff0000)
    return e

WHITELIST = ["177486429780312064"]

async def run(ctx,*args):
    if str(ctx.author.id) not in WHITELIST:
        user = await discord_integration.get_user_by_id(ctx, "177486429780312064")
        await discord_integration.send_message(ctx, None, error(f"This is an owner-only command. Only {user.mention} can use this command."))
    remove_files_by_pattern("./","*scoreboard.png")
    e = new_embed("Clean (OWNER ONLY)","The scoreboards have been cleaned.",0x00ff00)
    await discord_integration.send_message(ctx,None,e)