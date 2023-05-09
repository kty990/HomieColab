import sys
import os
import discord

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import discord_integration
from src.lib.embed import new_embed
from src.lib.scoreboard import Scoreboard
from src.lib import scoreboard
from src.lib.util import remove_files_by_pattern

async def run(ctx, *args):
    if len(args)%2 == 1:
        raise Exception("Must have even number of arguments to run -img")
    for i in range(0,len(args),2):
        s = Scoreboard()
        scoreboard.scoreboards.append(s)
        await s.create(args[i],args[i+1])
        i += 2
    sb = scoreboard.scoreboards[0]
    await sb.stack(*scoreboard.scoreboards)

    final_img = discord.File(str(sb.id) + 'stacked_scoreboard.png', filename=f"{str(sb.id)}stacked_scoreboard.png")
    e = new_embed("Img Used!","Dynamic Image Creation Test Command",0xccffcc)
    e.set_image(url=f"attachment://{str(sb.id)}stacked_scoreboard.png")
    await discord_integration.send_message(ctx,None,e,file=final_img)