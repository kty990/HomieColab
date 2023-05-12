import sys
import os
import discord

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import discord_integration
from src.lib.embed import new_embed
from src.lib.scoreboard import Scoreboard
from src.lib import scoreboard
from src.lib.util import remove_files_by_pattern

description = """Creates a scoreboard based on provided input. Must have equal number of arguments (ie. 2, 4, 6, etc.)"""

async def run(ctx, *args):
    if len(args)%2 == 1:
        raise Exception("Must have even number of arguments to run -img")
    sbs = []
    for i in range(0,len(args),2):
        s = Scoreboard()
        scoreboard.scoreboards.append(s)
        sbs.append(s)
        if i == 0:
            await s.create(args[i],args[i+1],(235, 198, 52))
        elif i == 2:
            await s.create(args[i],args[i+1],(201, 200, 201))
        elif i == 4:
            await s.create(args[i],args[i+1],(125, 98, 39))
        else:
            await s.create(args[i],args[i+1])
    
    sb = sbs[0]
    await sb.stack(*sbs)

    final_img = discord.File(str(sb.id) + 'stacked_scoreboard.png', filename=f"{str(sb.id)}stacked_scoreboard.png")
    
    e = new_embed("Img Used!","Dynamic Image Creation Test Command",0xccffcc)
    e.set_image(url=f"attachment://{str(sb.id)}stacked_scoreboard.png")
    await discord_integration.send_message(ctx,None,e,file=final_img)

    for x in sbs:
        remove_files_by_pattern("./",f"{str(x.id)}scoreboard.png")