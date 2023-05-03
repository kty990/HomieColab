import random
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib import discord_integration
from src.lib.embed import new_embed

description = """Test all required permissions for the bot."""

async def run(ctx, *args):
    status = ''
    # Send Messages
    x_emoji = await discord_integration.get_emoji(ctx,989702490209534004)
    msg = None
    try:
        msg = await discord_integration.send_message(ctx,".",None)
        status += "Send Messages: ✅"
    except:
        status += f"Send Messages: {x_emoji}"
    # Edit Messages
    try:
        await discord_integration.edit_message(msg,"..",None)
        status += "\nEdit (own) Messages: ✅"
    except:
        status += f"\nEdit (own) Messages: {x_emoji}"
    
    # React to Messages
    try:
        await discord_integration.add_reaction_(ctx,msg,"✅",None)
        status += "\nAdd Reaction: ✅"
    except:
        status += f"\nAdd Reaction: {x_emoji}"

    # Send Embeds
    try:
        message = await discord_integration.send_message(ctx,None,new_embed("Test","Test",0xff00ff))
        await message.delete()
        status += "\nSend Embeds: ✅"
    except:
        status += f"\nSend Embeds: {x_emoji}"
    # Delete (own) Messages
    try:
        await msg.delete()
        status += "\nDelete (own) Messages: ✅"
    except:
        status += f"\nDelete (own) Messages: {x_emoji}"

    try:
        await ctx.guild.me.edit(nick="test[-] Game Bot")
        await ctx.guild.me.edit(nick="[-] Game Bot")
        status += "\nChange (own) Nickname: ✅"
    except:
        status += f"\nChange (own) Nickname: {x_emoji}"

    try:
        if ctx.author.voice is None:
            raise Exception("<template>")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            try:
                await voice_channel.connect()
                status += f"\nJoin Voice Channel: ✅"
            except:
                status += f"\nJoin Voice Channel: {x_emoji}"
        else:
            #mod this to prevent moving to another voice channel
            status += f"\nJoin Voice Channel: ⚠️"
            #await ctx.voice_client.move_to(voice_channel)
    except:
        status += f"\nJoin Voice Channel: ⚠️"
    
    await discord_integration.send_message(ctx,None,new_embed("Test Results",status))