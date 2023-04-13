import sys
import os
import importlib
import discord
from datetime import datetime as date

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

description = """What do you need help with?"""

class Commands: 
    def __init__(self):
        self.commands = {} # {"COMMAND_NAME":MODULE}
        self.loaded = False
    
    def __repr__(self):
        keys = list(self.commands.keys())
        values = list(self.commands.values())
        result = "<<\n"
        for x in range(len(keys)):
            result = result + f"{keys[x]}:{values[x]}\n"
        return result + ">>"

    def add_command(self, module_name):
        print(f"Attempting to add {module_name}")
        try:
            if module_name == 'cmds':
                self.commands['cmds'] = "PLACEHOLDERVALUE"
                return
            commands_directory = './src/commands/'
            package_name = 'commands'
            module_fullname = f"{package_name}.{module_name}"
            module = importlib.import_module(module_fullname, commands_directory)
            self.commands[module_name] = module
        except Exception as e:
            print(e)

CommandObject = Commands()

directory = './src/commands'
file_list = os.listdir(directory)
print(f"File list: {file_list}")

for file in file_list:
    if os.path.isfile(os.path.join(directory, file)):
        if str(file).startswith("__"):
            continue
        else:
            CommandObject.add_command(str(file).replace(".py",""))

CommandObject.loaded = True

print(CommandObject.commands)

f_string = """**`%s`**
    • **Description:** `%s`

"""

async def run(ctx, *args):
    if not CommandObject.loaded:
        await ctx.send("An error has occured trying to run 'cmds'.")
        return
    output = ""
    for (command,module) in CommandObject.commands.items():
        print(type(command), type(module))
        if command == "cmds":
            output += f"{f_string % ('cmds',description or '<< description unavailable >>')}"
        else:
            output += f"{f_string % (command,module.description or '<< description unavailable >>')}"
    e = discord.Embed(title="Commands", description=output, color=0x00000)
    e.set_footer(text=f"{ctx.bot.user}")

    avatar_url = ""
    try:
        avatar_url = f"{str(ctx.author.avatar.url)}"
    except Exception as e:
        print(e)
        pass

    e.set_image(url=avatar_url)
    e.set_author(name=f"{ctx.author}", icon_url=f"{avatar_url}")
    e.timestamp = date.now()
    await ctx.send(embed=e)