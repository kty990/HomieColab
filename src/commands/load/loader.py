import sys
import os
import importlib

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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

    def add_command(self, command):
        try:
            commands_directory = './src/commands'
            module_name = os.path.splitext(command)[0] # Remove .py extension from filename
            package_name = 'commands' # Assuming 'commands' is the name of the package that contains the command modules
            self.commands[command] = importlib.import_module(f"{package_name}.{module_name}", commands_directory)
        except Exception as e:
            print(e)

CommandObject = Commands()

directory = './src/commands'
file_list = os.listdir(directory)

for file in file_list:
    if os.path.isfile(os.path.join(directory, file)):
        if str(file).startswith("__"):
            continue
        else:
            CommandObject.add_command(str(file).replace(".py",""))

CommandObject.loaded = True