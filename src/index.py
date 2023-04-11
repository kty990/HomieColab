import os
import discord
import json
from lib import util
from discord.ext import commands

# Get the absolute path of the auth.json file
auth_file = os.path.join(os.path.dirname(__file__), 'auth.json')

# Open the auth.json file and load the token
with open(auth_file, 'r') as f:
    data = json.load(f)
    token = data.get('token')

# Create intents object
intents = discord.Intents.default()

# Create bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define a command
@bot.command(name='hello')
async def hello(ctx):
    util.DEFAULT_COMMAND_ACTION(ctx)
    
@bot.command(name='coup')
async def coup(ctx):
    util.DEFAULT_COMMAND_ACTION(ctx)

# Run the bot
if token:
    bot.run(token)
else:
    print("Error: Token not found in .auth.json")