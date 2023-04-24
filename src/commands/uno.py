import random
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event

"""
TODO:
    - Complete GetPlayers() function
    - Complete game logic loop
    - Complete the Deck class
"""

"""
ACCEPTED ACTIONS:
- Tax
- Assassinate
- Steal
- Exchange
- Block
- Take 1 coins (aka. _____)
- Take 2 coins (aka. _____)
- coup

ACCEPTED COUNTER-ACTIONS:
- Block assassination (Contessa)
- Block steal (captain/ambassador)
- Block taking 2 coins (Duke)
"""

characters = {
    'Duke': '**Tax** (Take 3 coins from the treasury)',
    'Assassin': '**Assassinate** (Pay 3 coins to eliminate a player\'s influence)',
    'Captain': '**Steal** (Take 2 coins from another player)',
    'Ambassador': '**Exchange** (Trade in 2 cards from the deck)',
    'Contessa': '**Block** (Block an assassination attempt)',
    'Dead': 'n/a'
}

description = """WIP."""

class Player:
    def __init__(self, user):
        self.user = user #of type discord user
        self.cards = []

    def ComputeActions(self):
        actions = ""
        for card in self.cards:
            r = f"\t{card} : {characters[card]}\n"
            actions += r
        for key,value in characters.items():
            if not key in self.cards:
                r = f"\t{key} : {value} (⚠️)\n"
                actions += r
        return actions
    
    def MakeAction(self):
        pass

    def __repr__(self):
        return str(self.user)

class Deck:
    def __init__(self):
        self.cards = []
        self.NUM_OF_CARD_IN_DECK = 3 #Number of each character in the deck
    
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

async def GetPlayers(ctx, MAX_PLAYERS):
    #Requires Player object
    global MESSAGE_ID,START_CHECK

    MULTIPLIER = 2
    TIME_IN_SECONDS = 10

    message = await ctx.send(f"React with 👍 to join the game of coup!\nA maximum of {MAX_PLAYERS} players can join!\nYou have **{TIME_IN_SECONDS}** seconds left to react!")
    await message.add_reaction("👍")
    await message.add_reaction("⏯️")
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
            await message.edit(content=f"React with 👍 to join the game of coup!\nA maximum of {MAX_PLAYERS} players can join!\nYou have **{int(TIME_IN_SECONDS-((x/MULTIPLIER)+1))}** seconds left to react!")

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
        ctx.send("Sorry, a game is already in progress!")
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

    async def TakeTurn(player):
        if player.cards == []:
            player.cards.append(d.draw_card())
            player.cards.append(d.draw_card())
        actions = player.ComputeActions()
        separator = '\t&\t'
        await player.user.send(f"Here are your cards:\n{separator.join(player.cards)}\nYour available actions are:\n{actions}")
        action = await player.MakeAction() ################################################################### NOT COMPLETED ################################################################################
        quit() #ONLY FOR TESTING PURPOSES
        return action

    # define the main game loop
    current_player = 0
    while len(players) > 1:
        player = players[current_player]
        result = await TakeTurn(player)
        await ctx.send(f"{player} chose to {result}")
        current_player = (current_player + 1) % len(players)

    # determine the winner
    if len(players) == 1:
        await ctx.send(f"{players[0].user.mention} wins!")
    else:
        await ctx.send("It's a tie!")
    
    GAME_IN_PROGRESS = False
    START_CHECK = False
    STARTED_BY_ID = None
    event.USER_REACTED.remove_handler(reaction_handle)
    event.USER_UNREACTED.remove_handler(unreaction_handle)