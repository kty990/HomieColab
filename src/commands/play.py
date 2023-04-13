import os
import re
import asyncio
import pytube
from discord.utils import get
import discord

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

class Node:
     def __init__(self, next=None, prev=None, data=None):
          self.next = next
          self.prev = prev
          self.data = data

class EMPTY_QUEUE_EXCEPTION(Exception):
    def __init__(self):
        pass

class Queue:
    def __init__(self):
        self.root = None
    
    def enqueue(self,data):
        tmp = self.root
        while tmp.next != None:
            tmp = tmp.next
        tmp.next = Node(None,self.root,data)

    def dequeue(self):
        if self.isEmpty():
            raise EMPTY_QUEUE_EXCEPTION("Can't dequeue from an empty queue")
        tmp = self.root
        if self.root.next:
            self.root = self.root.next
            self.root.prev = None
        return tmp
    
    def isEmpty(self):
        return self.root == None
     

class Music:
    """
    ctx - Context
        : Required for initialization
    """
    def __init__(self, ctx):
        self.queue = Queue()
        self.bot = ctx.bot

        @self.bot.event
        async def on_voice_state_update(member, before, after):
            if member == self.bot.user and not after.channel:
                try:
                    ctx.voice_client.pause()
                    print("Paused")
                except Exception:
                    pass
            else:
                try:
                    if (ctx.voice_client.is_paused()):
                        ctx.voice_client.resume()
                        print("resuming...")
                except Exception:
                    pass


    async def play(self,ctx,url):
        guild = ctx.guild
        vc = get(ctx.bot.voice_clients, guild=guild)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return
        if vc is None:
            try:
                vc = await voice_channel.connect()
            except Exception:
                raise Exception("Unable to connect to voice channel. > PLAY")
        try:
            video = pytube.YouTube(url)
            audio_url = video.streams.filter(only_audio=True).first().url
        except:
            await ctx.send("Unable to get audio URL from the given URL.")
            return

        vc.play(discord.FFmpegPCMAudio(audio_url))
        ctx.playing = True
        while vc.is_playing():
            await asyncio.sleep(1)
        ctx.playing = False
        if (not vc.is_paused()):
            await self.next(ctx)

    async def next(self, ctx):
        # If there's a song in the queue, play it next
        if not self.queue.isEmpty():
            next_url = self.queue.dequeue()
            self.play(ctx, next_url)

async def run(ctx, *args):
    if not ctx.queues:
        ctx.playing = False
        ctx.queues = {}
    if not ctx.guild.id in ctx.queues:
        ctx.queues[ctx.guild.id] = Music(ctx)
    validUrls = []
    for arg in args:
        if (validURL(arg)):
            validUrls.append(arg)
    
    for url in validUrls:
        await ctx.queues[ctx.guild.id].play(ctx,url)
    
    