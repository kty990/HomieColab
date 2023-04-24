import sys
import os
import importlib
import discord
from datetime import datetime as date

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

os.chdir('c:/Users/maste/Desktop/coup/HomieColab')

# print(sys.path)

description = """Commands for you to use can be found with this command."""

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
        # print(f"Attempting to add {module_name}")
        try:
            if module_name == 'cmds':
                self.commands['cmds'] = "PLACEHOLDERVALUE"
                return
            directory = '/src/commands/'
            absolute_path = None
            if os.getcwd().endswith("coup"):
                #On Computer-Ty
                absolute_path = os.path.abspath(os.path.join(os.getcwd(), f"./HomieColab{directory}"))
            elif os.getcwd().endswith("HomieColab"):
                #On Computer-Ty or other
                absolute_path = os.path.abspath(os.path.join(os.getcwd(), f".{directory}"))
            else:
                #On other
                absolute_path = os.path.abspath(os.path.join(os.getcwd(), f"../{directory}"))
            # print(absolute_path)
            package_name = 'commands'
            module_fullname = f"{package_name}.{module_name}"
            module = importlib.import_module(module_fullname, absolute_path)
            self.commands[module_name] = module
        except Exception as e:
            print(f"Exception occured on add_command @ cmds.py:\n{e}")

CommandObject = Commands()

directory = '/src/commands/'
absolute_path = None
if os.getcwd().endswith("coup"):
    #On Computer-Ty
    absolute_path = os.path.abspath(os.path.join(os.getcwd(), f"./HomieColab{directory}"))
elif os.getcwd().endswith("HomieColab"):
    #On Computer-Ty or other
    absolute_path = os.path.abspath(os.path.join(os.getcwd(), f".{directory}"))
else:
    #On other
    absolute_path = os.path.abspath(os.path.join(os.getcwd(), f"../{directory}"))
file_list = os.listdir(absolute_path)
# print(f"File list: {file_list}")

for file in file_list:
    if os.path.isfile(os.path.join(absolute_path, file)):
        if str(file).startswith("__"):
            continue
        else:
            CommandObject.add_command(str(file).replace(".py",""))

CommandObject.loaded = True

# print(CommandObject.commands)

f_string = """**`%s`**
    • **Description:** `%s`

"""

async def run(ctx, *args):
    if not CommandObject.loaded:
        await ctx.send("An error has occured trying to run 'cmds'.")
        return
    output = ""
    for (command,module) in CommandObject.commands.items():
        # print(type(command), type(module))
        if command == "cmds":
            output += f"{f_string % ('cmds',description or '<< description unavailable >>')}"
        else:
            output += f"{f_string % (command,module.description or '<< description unavailable >>')}"
    e = discord.Embed(title="Commands", description=output, color=0x00000)
    e.set_footer(text=f"{ctx.bot.user}")
    # print(output)
    avatar_url = f"{str(ctx.author.avatar.url)}"

    e.set_image(url=avatar_url)
    e.set_author(name=f"{ctx.author}", icon_url=f"{avatar_url}")
    e.timestamp = date.now()
    await ctx.send(embed=e)