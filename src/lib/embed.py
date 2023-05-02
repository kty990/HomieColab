from discord import Embed
from datetime import datetime

def new_embed(title="",description="", color=0xffffff):
    return Embed(title=title,description=description,colour=color)#,timestamp=datetime.now())