import os

description = """Makes the bot disconnect from its current voice channel."""

async def run(ctx, *args):
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel")
        return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected.")