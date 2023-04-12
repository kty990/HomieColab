import os
import discord
import json
from lib import util
from commands.load import loader
from discord.ext.commands import Command
from discord.ext import commands

auth_file = os.path.join(os.path.dirname(__file__), 'auth.json')
cmds = {}

with open(auth_file, 'r') as f:
    data = json.load(f)
    token = data.get('token')

intents = discord.Intents.default()
intents.members = True  # Enable the members intent
intents.message_content = True  # Enable the messages intent

bot = commands.Bot(command_prefix='', intents=intents)

ii = 0
while not loader.CommandObject.loaded:
    if ii % 10 == 0:
        print("Loading...")
    ii += 1

for module_name, module in loader.CommandObject.commands.items():
    command_func = Command(module.run, name=f"-{module_name}")
    bot.add_command(command_func)
    cmds[module_name] = command_func

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # ignore command not found errors

    # log the error to the console
    print(f"An error occurred: {error}")

    # send a message to the user
    await ctx.send("An error occurred while processing your command. Please try again later.")


if token:
    bot.run(token)
else:
    print("Error: Token not found in .auth.json")