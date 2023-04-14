from discord.utils import get
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import util
from src.lib import music

description = """Pauses the track if one is playing."""

async def run(ctx, *args):
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN
    # music.musics[ctx.guild.id]['music'] = music.Music(ctx)
    # music.musics[ctx.guild.id]['playing'] = False

    assert ctx.guild.id in music.musics, "An unknown error occurred."
    

    if not music.musics[ctx.guild.id]['playing']: 
        ctx.send("Unable to pause if no sound is playing.")
    else:
        try:
            ctx.voice_client.pause()
            ctx.send("Paused.")
            music.musics[ctx.guild.id]['playing'] = False
        except Exception as e:
            ctx.send("An error occured trying to run your command.")
            print(e)
            
    
    