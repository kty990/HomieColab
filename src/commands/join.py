import os

description = """Makes the bot join the channel the user is in."""

async def run(ctx, *args):
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel")
        return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        #mod this to prevent moving to another voice channel
        await ctx.voice_client.move_to(voice_channel)