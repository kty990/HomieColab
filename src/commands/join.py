import os

async def run(ctx, *args):
    print("JOIN USED CONFIRM")
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel")
        return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        print(ctx.voice_client)
        await ctx.voice_client.move_to(voice_channel)