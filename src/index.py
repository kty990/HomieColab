import os
import sys
import discord
import json
from commands.load import loader
from discord.ext.commands import Command
from discord.ext import commands

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib import discord_integration
from src.lib.embed import new_embed

auth_file = os.path.join(os.path.dirname(__file__), 'auth.json')
cmds = {}

PREFIX = "-"

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
    async def command_func(ctx, *args, module=module, module_name=module_name):
        print(f'{module_name} used!')
        await module.run(ctx, *args)
    bot.add_command(Command(command_func, name=f"{PREFIX}{module_name}"))
    cmds[module_name] = command_func

######################### EVENTS ############################

@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandNotFound):
        return  # ignore command not found errors

    # log the error to the console
    print(f"An error occurred: {error}")

    # send a message to the user
    err = str(error)
    if len(err) > 150:
        err = err[:150] + "  (...) omitted some output"
    e = new_embed("Error!","An error occurred while processing your command. Please try again later.",0xff0000)
    e.add_field(name="\u2800",value=err,inline=False)
    await discord_integration.send_message(ctx,None,e)

@bot.event
async def on_reaction_add(reaction,user):
    event.USER_REACTED.fire(reaction=reaction,user=user)

@bot.event
async def on_reaction_remove(reaction,user):
    event.USER_UNREACTED.fire(reaction=reaction,user=user)

######################### START ############################

if token:
    bot.run(token)
else:
    print("Error: Token not found in .auth.json")

