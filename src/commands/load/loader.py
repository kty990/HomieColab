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

    def add_command(self, module_name):
        try:
            commands_directory = './HomiesColab/src/commands'
            package_name = 'commands'
            module_fullname = f"{package_name}.{module_name}"
            module = importlib.import_module(module_fullname, commands_directory)
            self.commands[module_name] = module
        except Exception as e:
            print(e)

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

# print(absolute_path)
file_list = os.listdir(absolute_path or directory or "")

for file in file_list:
    # print(f"FILE: {str(file)}")
    if os.path.isfile(os.path.join(absolute_path or directory or "", file)):
        if str(file).startswith("__"):
            continue
        else:
            # print(f"Adding {str(file)}...")
            CommandObject.add_command(str(file).replace(".py",""))

CommandObject.loaded = True
print("Loaded...")