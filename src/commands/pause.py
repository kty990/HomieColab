from discord.utils import get

async def run(ctx, *args):
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN
    if not ctx.playing: 
        ctx.send("Unable to pause if no sound is playing.")
    else:
        try:
            ctx.voice_client.pause()
            ctx.send("Paused.")
        except Exception as e:
            ctx.send("An error occured trying to run your command.")
            print(e)
            
    
    