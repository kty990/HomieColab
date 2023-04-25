import random
import asyncio
import sys
import os
from discord import DMChannel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib.word_aliases import yes
from src.lib.embed import new_embed

"""
TODO:
    - Complete GetPlayers() function | X
    - Complete game logic loop       |
    - Complete the Deck class        |
"""

"""
ACCEPTED ACTIONS:
- Tax
- Assassinate
- Steal
- Exchange
- Take 1 coins (aka. Income)
- Take 2 coins (aka. Foreign Aid)
- coup

ACCEPTED COUNTER-ACTIONS:
- Block assassination (Contessa)
- Block steal (captain/ambassador)
- Block foreign aid (Duke)
"""

characters = {
    'Duke': '**Tax** (Take 3 coins from the treasury)',
    'Assassin': '**Assassinate** (Pay 3 coins to eliminate a player\'s influence)',
    'Captain': '**Steal** (Take 2 coins from another player)',
    'Ambassador': '**Exchange** (Trade in 2 cards from the deck)',
    'Contessa': '**Block** (Block an assassination attempt)'
}

description = """WIP."""

class Player:
    def __init__(self, user):
        self.user = user #of type discord user
        self.cards = []
        self.influence = 2
        self.coins = 2
        self.valid_actions = {
            'tax':self.tax,
            'assassinate':self.assassinate,
            'steal':self.steal,
            'exchange':self.exchange,
            'income':self.income,
            'foreign aid':self.foreign_aid,
            'coup':self.coup,
        }
        self.valid_counters = {
            'assassination':['contessa'],
            'steal':['captain','ambassador'],
            'foreign aid':['duke']
        }

    def coup(self):
        # Cannot be challenged
        pass

    async def foreign_aid(self):
        # Can be blocked
        """ Check if anyone wants to block """
        """ If yes, check if self wants to challenge the block --- If no, skip turn"""
        """ If self wants to challenge the block, check to see if the player wants to reveal their card (if they can) """
        self.coins += 2
        pass

    def income(self):
        self.coins += 1
        pass

    def tax(self, player):
        # Can be challenged
        self.coins += 3
        pass

    def eliminate(self, player):
        # Eliminate 1 influence
        player.influence -= 1
        """ Prompt target for which card they want to get rid of if they have 2 cards, otherwise they are dead """
        pass

    async def assassinate(self, player):
        # Can be blocked
        """ Check if target wants to block """
        """ If yes, check if self wants to challenge the block --- If no, eliminate()"""
        """ If self wants to challenge the block, check to see if the player wants to reveal their card (if they can) """
        
        pass

    async def steal(self, player):
        # Can be blocked
        """ Check if target wants to block """
        """ If yes, check if self wants to challenge the block --- If no:
                                player.coins -= 2 ----- self.coins += 2"""
        """ If self wants to challenge the block, check to see if the player wants to reveal their card (if they can) """
        pass

    async def exchange(self, deck):
        # Can be challenged
        cards = deck.draw_cards(2)
        card_pool = []
        for x in cards:
            card_pool.append(x)
        for x in self.cards:
            card_pool.append(x)
        prompt = "\n- ".join([x.upper() for x in card_pool])
        e = new_embed("COUP - Exchange",f"Pick 2 of the following cards to keep, the other 2 will be discarded!\n- {prompt}")
        message = await self.user.send(embed=e)
        
        
        """ REQUIRES SOME FORM OF REACTION """
        reactions = {
            "1️⃣":card_pool[0],
            "2️⃣":card_pool[1],
            "3️⃣":card_pool[2],
            "4️⃣":card_pool[3],
        }

        for reaction in reactions.keys():
            await message.add_reaction(reaction)
        
        # let the player choose which cards to keep
        # and which to return to the deck

    def ComputeActions(self):
        actions = ""
        for card in self.cards:
            r = f"\t{card} : {characters[card]}\n"
            actions += r
        for key,value in characters.items():
            if not key in self.cards:
                r = f"\t{key} : {value} (⚠️)\n"
                actions += r
        actions += f"**Income** : Take 1 coin\n**Foreign Aid** : Take 2 coins"
        return actions
    
    async def MakeAction(self, ctx, player_list):
        def check(message):
            return isinstance(message.channel, DMChannel) and message.author.id == self.user.id

        e = new_embed("COUP",f"What do you choose to do?")
        message = await self.user.send(embed=e)
        response = await ctx.bot.wait_for('message', check=check, timeout=None)
        target = None
        i = 1
        while response.content.lower() not in self.valid_actions.keys():
            i += 1
            await response.delete()
            e.description = f"Attempt #{i}\nThat is not a valid action. Valid actions include any of the bolded actions:\n{self.ComputeActions()}"
            await message.edit(embed=e)
       
        if response.content.lower() in ['assassinate','steal','coup']:
            players_prompt = '\n- '.join([str(x)[:-5] for x in player_list])
            e = new_embed("COUP",f"Who do you to want to {response.content.lower()}?\nValid options include: \n- {players_prompt}")
            await self.user.send(embed=e)
            target = await ctx.bot.wait_for('message', check=check, timeout=None)
            i = 1
            while not target.content.lower() in [str(x).lower()[:-5] for x in player_list]: #list comp for player user tags
                i += 1
                players_prompt = '\n- '.join([str(x)[:-5] for x in player_list])
                e.description = f"Attempt #{i}\nWho do you to want to {response.content.lower()}?\nValid options include: \n- {players_prompt}"
                await message.edit(embed=e)
                target = await ctx.bot.wait_for('message', check=check, timeout=None)
        
            for x in player_list:
                if str(x)[:-5].lower() == target.content.lower():
                    target = x
                    break

        # Now check if anyone wants to challenge the action, give 10 seconds
        challenged = None
        for player in player_list:
            if player.user.id != self.user.id:
                def check2(user):
                    def inner(message):
                        return message.author.id == user.id and isinstance(message.channel, DMChannel)
                    return inner 
                e = new_embed("COUP",f"{str(self.user)} chose to {response.content.lower()}, do you wish to challenge?")
                message = await player.user.send(embed=e)
                try:
                    response = await ctx.bot.wait_for('message', check=check2(player.user), timeout=10)
                    if response in yes:
                        challenged = player.user
                except:
                    pass
        await asyncio.sleep(10)
        if challenged:
            e = new_embed("COUP",f"{challenged} challenged {self.user}")
            await ctx.send(embed=e)
            # Does the user want to reveal their card, or pretend they don't have it/acknowledge they don't have it
            # if the challenge succeeds, THIS player loses 1 influence/dies if they only had 1 left
            # ^and then return the action as a string
            pass
        
        #If the action is block-able, check with the target if they want to claim they can block
        pass


    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
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
    
    def refresh(self, characters: dict):
        #Populate deck
        for x in list(characters.keys()) * self.NUM_OF_CARD_IN_DECK:
            self.cards.append(x)

"""
Creates a 'join prompt' in the server's channel that this was sent from.
Requires reaction to join, unreact to un-join
"""

GAME_IN_PROGRESS = False
START_CHECK = False
REACTIONS = []
MESSAGE_ID = None
STARTED_BY_ID = None

"""
0 - Not active
1 - Game requested, gathering players
2 - Game in progress
"""
GAME_STAGE = 0

def check(reaction, user):
        client = reaction.message.author
        return str(reaction.emoji) == "👍" and user.id != client.id

async def GetPlayers(ctx, MAX_PLAYERS):
    #Requires Player object
    global MESSAGE_ID,START_CHECK

    MULTIPLIER = 2
    TIME_IN_SECONDS = 10

    e = new_embed('COUP',f"React with 👍 to join the game of coup!\nA maximum of {MAX_PLAYERS} players can join!\nYou have **{TIME_IN_SECONDS}** seconds left to react!")
    message = await ctx.send(embed=e)
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
            e.description = f"React with 👍 to join the game of coup!\nA maximum of {MAX_PLAYERS} players can join!\nYou have **{int(TIME_IN_SECONDS-((x/MULTIPLIER)+1))}** seconds left to react!"
            await message.edit(embed=e)

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
    global GAME_IN_PROGRESS, STARTED_BY_ID, START_CHECK, GAME_STAGE
    if GAME_IN_PROGRESS:
        await ctx.send("Sorry, a game is already in progress!")
        return
    STARTED_BY_ID = ctx.author.id
    GAME_STAGE = 1
    GAME_IN_PROGRESS = True
    event.USER_REACTED.add_handler(reaction_handle)
    event.USER_UNREACTED.add_handler(unreaction_handle)
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN

    d = Deck()
    d.refresh(characters=characters)

    #Get players
    players = await GetPlayers(ctx, 6)
    if len(players) < 2:
        e = new_embed("COUP","Sorry, not enough players joined!")
        await ctx.send(embed=e)
        return

    GAME_STAGE = 2   
    
    #Shuffle the deck
    d.shuffle()

    async def TakeTurn(player):
        if player.cards == []:
            player.cards.append(d.draw_card())
            player.cards.append(d.draw_card())
        actions = player.ComputeActions()
        separator = '\t&\t'
        e = new_embed("COUP",f"Here are your cards:\n{separator.join(player.cards)}\nYour available actions are:\n{actions}")
        await player.user.send(embed=e)
        action = await player.MakeAction(ctx, players) ################################################################### NOT COMPLETED ################################################################################
        quit() #ONLY FOR TESTING PURPOSES
        return action

    # define the main game loop
    current_player = 0
    while len(players) > 1:
        player = players[current_player]
        result = await TakeTurn(player)
        e = new_embed("COUP",f"{player} chose to {result}")
        await ctx.send(embed=e)
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