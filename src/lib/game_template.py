import random
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib import discord_integration
from src.lib.embed import new_embed

description = """WIP."""

class Player:
    def __init__(self, user):
        pass

    def __repr__(self):
        return "<Player TEMPLATE>"

class Deck:
    def __init__(self):
        self.cards = []
    
    def __repr__(self):
        return "<Deck TEMPLATE>"
    
    def shuffle(self):
        tmp = []
        for x in self.cards:
            tmp.append(self.cards.pop(random.randint(0,len(self.cards)-1)))
        self.cards = tmp

    def draw_cards(self, num: int = 0):
        cards = []
        for x in range(num):
            cards.append(self.cards.pop())
        return cards

    def draw_card(self):
        return self.cards.pop()
    
    def populate(self):
        #Populate deck
        pass

"""
Creates a 'join prompt' in the server's channel that this was sent from.
Requires reaction to join, unreact to un-join
"""

GAME_IN_PROGRESS = False
START_CHECK = False
REACTIONS = []
MESSAGE_ID = None
STARTED_BY_ID = None

def check(reaction, user):
        client = reaction.message.author
        return str(reaction.emoji) == "👍" and user.id != client.id

async def GetPlayers(ctx, game_title, MAX_PLAYERS):
    #Requires Player object
    global MESSAGE_ID,START_CHECK

    MULTIPLIER = 2
    TIME_IN_SECONDS = 10


    e = new_embed("<template>","<template>")
    message = await discord_integration.send_message(ctx, "<template>", e)
    await discord_integration.add_reaction("👍")
    await discord_integration.add_reaction("⏯️")
    MESSAGE_ID = message.id
    # Wait for 60 seconds to allow for users to join
    for x in range(TIME_IN_SECONDS*MULTIPLIER):
        await asyncio.sleep(1/MULTIPLIER)
        if len(REACTIONS) == MAX_PLAYERS or START_CHECK:
            START_CHECK = False
            players = []
            for value in REACTIONS:
                players.append(Player(value['user']))
            await message.delete()
            MESSAGE_ID = None
            return players
        if x % MULTIPLIER == 0:
            e = new_embed("<template>","<template>")
            await discord_integration.edit_message(message=message,new_embed=e)

    players = []
    for value in REACTIONS:
        players.append(Player(value['user']))
    return players

def allow_start(reaction,user):
    return str(reaction.emoji) == "⏯️" and user.id == STARTED_BY_ID

def reaction_handle(reaction,user):
    global START_CHECK
    try:
        msg = reaction.message
        if msg.id == MESSAGE_ID and check(reaction,user):
            print(f"{user} REACTED")
            REACTIONS.append({
                'user':user,
                'reaction':reaction
            })
        elif msg.id == MESSAGE_ID and allow_start(reaction,user):
            START_CHECK = True
        else:
            print(f"{user} REACTED WITH {str(reaction)} BUT IT DOESN'T SEEM TO BE VALID...")
    except Exception as e:
        print(e)

def unreaction_handle(reaction,user):
    try:
        msg = reaction.message
        if msg.id == MESSAGE_ID and check(reaction,user):
            print(f"{user} UNREACTED")
            for x in REACTIONS:
                if x['user'] == user and x['reaction'] == reaction:
                    REACTIONS.remove(x)
                    print("REACTION REMOVED")
                    break
        else:
            print(f"{user} REACTED WITH {str(reaction)} BUT IT DOESN'T SEEM TO BE VALID...")
    except Exception as e:
        print(e)

async def run(ctx, *args):
    global GAME_IN_PROGRESS, STARTED_BY_ID, START_CHECK
    if GAME_IN_PROGRESS:
        await discord_integration.send_message(ctx,prompt="Sorry, a game is already in progress!")
        return
    STARTED_BY_ID = ctx.author.id
    GAME_IN_PROGRESS = True
    event.USER_REACTED.add_handler(reaction_handle)
    event.USER_UNREACTED.add_handler(unreaction_handle)
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN

    d = Deck()
    d.populate()

    #Get players
    players = await GetPlayers(ctx, 6)
    print(players)

    """ GAME LOGIC HERE """
    
    GAME_IN_PROGRESS = False
    START_CHECK = False
    STARTED_BY_ID = None
    event.USER_REACTED.remove_handler(reaction_handle)
    event.USER_UNREACTED.remove_handler(unreaction_handle)