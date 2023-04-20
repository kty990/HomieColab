import os
import re
from discord.utils import get
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import util
from src.lib import music

description = """Attempts to play soundtracks given by URL. WIP : Will include play by query"""

current_file = os.path.basename(__file__)
def validURL(url):
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # scheme
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return url_regex.match(url) is not None

async def run(ctx, *args):
    if not ctx.guild.id in music.musics:
        music.musics[ctx.guild.id] = {}
        music.musics[ctx.guild.id]['music'] = music.Music(ctx)
        music.musics[ctx.guild.id]['playing'] = False
    
    validUrls = []
    a = list(args)
    for arg in args:
        u = await util.GenerateURL(arg)
        if (validURL(u)):
            validUrls.append(u)

    for url in validUrls:
        await music.musics[ctx.guild.id]['music'].play(ctx,url)