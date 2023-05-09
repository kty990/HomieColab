import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import discord_integration
from src.lib.embed import new_embed
from src.lib.scoreboard import Scoreboard
from src.lib import scoreboard

async def run(ctx, *args):
    s = Scoreboard()
    scoreboard.scoreboards.append(s)
    await s.create(args[0],args[1],args[2],args[3])
    img = s.get_image()
    await ctx.send(file=img)