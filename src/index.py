import os
import discord
import json
from lib import util
from commands.load import loader
from discord.ext import commands

auth_file = os.path.join(os.path.dirname(__file__), 'auth.json')
cmds = {}

with open(auth_file, 'r') as f:
    data = json.load(f)
    token = data.get('token')

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

while not loader.CommandObject.loaded:
    pass

for index, (command,module) in enumerate(loader.CommandObject.commands):
    @bot.command(name=command)
    async def run(ctx):
        module.run(ctx)
    cmds[command] = run

@bot.command(name='hello')
async def hello(ctx):
    util.DEFAULT_COMMAND_ACTION(ctx)
    
@bot.command(name='test')
async def test(ctx):
    util.DEFAULT_COMMAND_ACTION(ctx)

if token:
    bot.run(token)
else:
    print("Error: Token not found in .auth.json")