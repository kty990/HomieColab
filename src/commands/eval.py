import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib import discord_integration
from src.lib.embed import new_embed

description = """Evaluate a math expression."""

async def run(ctx, *args):
    expression = "".join(args)
    result = eval(expression)
    e = new_embed("Evaluate",f"{expression}={result}")
    await discord_integration.send_message(ctx,None,e)