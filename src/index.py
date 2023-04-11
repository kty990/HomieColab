import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello, world!')

bot.run('YOUR_BOT_TOKEN_HERE')