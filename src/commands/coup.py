# -*- coding: utf-8 -*-

import random
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib.embed import new_embed
from src.lib import discord_integration

"""
TODO:
    - Complete GetPlayers() function | X
    - Complete game logic loop       |
    - Complete the Deck class        | X
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
    'duke': '**Tax** (Take 3 coins from the treasury)',
    'assassin': '**Assassinate** (Pay 3 coins to eliminate a player\'s influence)',
    'captain': '**Steal** (Take 2 coins from another player)',
    'ambassador': '**Exchange** (Trade in 2 cards from the deck)',
    'contessa': '**n/a (only counter-action)** (Block an assassination attempt)'
}

description = """Play the classic card game Coup! on discord."""

def DEFAULT_ACTION():
    pass

async def block_function(self,valid_block,action=DEFAULT_ACTION,**kwargs):
    assert callable(action), "Action must be a function"
    e = new_embed("COUP - Block","React with 🛡️ to block the assassination attempt.\nYou have **10** seconds.")
    target = kwargs['target']
    ctx = kwargs['ctx']
    msg = await discord_integration.DM_no_response(ctx,target.user,None,e)
    await discord_integration.add_reaction_(ctx,msg,"🛡️",None)            
    reaction = discord_integration.wait_for_reaction_timeout(ctx,["🛡️"],[target.user],10)
        
    if reaction != None:
        user = await ctx.bot.fetch_user(reaction.user_id)
        e = new_embed("COUP - Blocked",f"{str(user)} has blocked {str(self.user)} from using assassination attempt. Waiting for response about challenging the block...")
        await discord_integration.send_message(ctx,None,e)
        e = new_embed("COUP - Action blocked",f"{str(user)} has blocked your assassination attempt. Do you challenge the block? (You have 10 seconds to decide)\nReact with ⚠️ to challenge. Do nothing and the block is automatically successful")
        msg = await discord_integration.DM_no_response(ctx,self.user,None,e)
        await discord_integration.add_reaction_("⚠️")
        reaction = await discord_integration.wait_for_reaction_timeout(ctx,['⚠️'],[self.user],10)
        if reaction:
            #Challenged
            e = new_embed("COUP - Block challenged!",f"{str(self.user)} challenges {str(user)}'s block. Awaiting response...")
            await discord_integration.send_message(ctx,None,e)
            def has_correct_card_to_block():
                return 'duke' in self.cards
                    
            prompt = f"{'have the correct card to block. React with any reaction to show the card and win the challenge. Do nothing and you lose the challenge and an influence.' if has_correct_card_to_block() else 'do not have the correct card to block. You lose the challenge!'}"
            e = new_embed("COUP - Block challenged!",f"{str(self.user)} challenges your block. You {prompt}.\nYou have **10** seconds.")
            msg = await discord_integration.DM_no_response(ctx,user,None,e)
            reaction = await discord_integration.wait_for_reaction_timeout(ctx,['⚠️'],[self.user],10)
            if reaction:
                #Check if the player that blocked had contessa
                if not valid_block:
                    #Challenge succeeds
                    action()
                else:
                    #Challenge fails, self instantly dies.
                    e = new_embed("COUP - Block challenge failed!",f"{str(self.user)} challenged {str(target.user)}'s block and loses the challenge.")
                    await discord_integration.send_message(ctx,None,e)
                    self.dead = True
            else:
                #Block successful
                action()
        else:
            action()

class Player:
    def __init__(self, user):
        self.user = user
        self.dead = False
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

    async def coup(self, **kwargs):
        # Cannot be challenged
        player_list = kwargs['player_list']
        ctx = kwargs['ctx']
        target_string = ""
        i = 1
        targets = {}
        for player in player_list:
            reaction_template = f"{chr(ord(str(i)))}\uFe0F\u20E3"
            targets[f"{reaction_template}"] = player.user
            target_string += f"{reaction_template} : {str(player.user)}"
            targets.append(reaction_template)
            i += 1
        target_embed = new_embed(name="COUP - Select a target!",value=target_string,inline=False)
        target_message = await discord_integration.DM_no_response(ctx,self.user,None,target_embed)
        for key in targets.keys():
            await target_message.add_reaction(key) # This may not work, may have to hard-code the emojis
        
        dm_channel = await self.user.create_dm()
        chosen_target = await discord_integration.wait_for_reaction(ctx,targets.keys(),self.user,dm_channel)
        targets[str(chosen_target)].eliminate()
        self.coins -= 7

    async def foreign_aid(self, **kwargs):
        target = kwargs['target']
        def action():
            self.coins += 2
        await block_function(self,'duke' in target.cards,action,kwargs=kwargs)

    def income(self, **kwargs):
        self.coins += 1
        pass

    def tax(self, **kwargs):
        self.coins += 3

    async def eliminate(self, **kwargs):
        # Eliminate 1 influence
        ctx = kwargs['ctx']
        self.influence -= 1
        if self.influence == 0:
            #This player is now dead
            self.dead = True
            e = new_embed("COUP - %s is out of influence" % str(self.user), f"The game carries on until 1 survives!")
            await discord_integration.send_message(ctx,None,e)
            return
        prompt = f"React with one of the following:\n1️⃣:{self.cards[0]}\n2️⃣:{self.cards[1]}"
        e = new_embed("COUP - Eliminate 1 influence",prompt)
        msg = discord_integration.DM_no_response(ctx,self.user,None,e)
        await discord_integration.add_reaction_(ctx,msg,'1️⃣',None)
        await discord_integration.add_reaction_(ctx,msg,'2️⃣',None)
        dm_channel = await self.user.create_dm()
        reaction = await discord_integration.wait_for_reaction(ctx,['1️⃣','2️⃣'],self.user,dm_channel,None)
        if str(reaction) == '1️⃣':
            self.cards[0] = '**dead**'
        else:
            self.cards[1] = '**dead**'

    async def assassinate(self, **kwargs):
        target = kwargs['target']
        def action():
            player = kwargs['target']
            player.eliminate(kwargs)
        await block_function(self,'contessa' in target.cards,action,kwargs=kwargs)

    async def steal(self, **kwargs):
        target = kwargs['target']
        def action():
            player = kwargs['target']
            player.coins -= 2 
            self.coins += 2
        await block_function(self,'captain' in target.cards or 'ambassador' in target.cards, action, kwargs=kwargs) 

    async def exchange(self, **kwargs):
        deck = kwargs['deck']
        ctx = kwargs['ctx']
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
        
        dm_channel = await self.user.create_dm()
        reaction = await discord_integration.wait_for_reaction(ctx, reactions.keys(),self.user,dm_channel)
        await message.clear_reaction(reaction)
        new_keys = reactions.keys()
        new_keys.remove(reaction)
        reaction2 = await discord_integration.wait_for_reaction(ctx, new_keys, self.user, dm_channel)
        new_keys.remove(reaction2)
        cards = []
        cards.append(reactions[reaction])
        cards.append(reactions[reaction2])
        for r in new_keys:
            deck.add_card(reactions[r])
        deck.shuffle()
        self.cards = cards

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
    
    async def MakeAction(self, ctx, player_list, deck):
        """ REQUIRES SOME FORM OF REACTION """
        target = None
        reactions = {
            "1️⃣":self.tax,
            "2️⃣":self.assassinate,
            "3️⃣":self.steal,
            "4️⃣":self.coup,
            "5️⃣":self.income,
            "6️⃣":self.foreign_aid,
            "7️⃣":self.exchange
        }

        e = new_embed("COUP",f"What do you choose to do?")
        prompt = """1️⃣ tax,
            2️⃣ assassinate,
            3️⃣ steal,
            4️⃣ coup,
            5️⃣ income,
            6️⃣ foreign_aid,
            7️⃣ exchange"""
        e.add_field(name="\u2800",value=prompt,inline=False)
        e.add_field(name="Choose one of the following:",value=self.ComputeActions(), inline=False)
        dm_channel = await self.user.create_dm()

        choice = await discord_integration.wait_for_reaction(ctx,reactions.keys(),self.user,dm_channel)
        if self.coins >= 10:
            #MUST coup
            group_e = new_embed("COUP - Action taken",f"{str(self.user)} has {self.coins} coins and must coup another player. Awaiting target selection.")
            await discord_integration.DM_no_response(ctx,self.user,f"Sorry but you have {self.coins} coins, you have to coup another player!",None)
            await discord_integration.send_message(ctx,None,group_e)
            target_string = ""
            i = 1
            targets = {}
            for player in player_list:
                reaction_template = f"{chr(ord(str(i)))}\uFe0F\u20E3"
                targets[f"{reaction_template}"] = player.user
                target_string += f"{reaction_template} : {str(player.user)}"
                targets.append(reaction_template)
                i += 1
            target_embed = new_embed(name="COUP - Select a target!",value=target_string,inline=False)
            target_message = await discord_integration.DM_no_response(ctx,self.user,None,target_embed)
            for key in targets.keys():
                await target_message.add_reaction(key) # This may not work, may have to hard-code the emojis

            chosen_target = await discord_integration.wait_for_reaction(ctx,targets.keys(),self.user,dm_channel)
            targets[str(chosen_target)].eliminate()
            self.coins -= 7
        else:
            message = await discord_integration.DM_no_response(ctx,self.user,None,e)
        
            for reaction in reactions.keys():
                await discord_integration.add_reaction_(ctx,message,reaction,None)

            """GET TARGET AND PERFORM ACTION"""
            if reactions[str(choice)].__name__.replace("_"," ") in ['assassinate','steal','coup']:
                target_string = ""
                i = 1
                targets = {}
                for player in player_list:
                    reaction_template = f"{chr(ord(str(i)))}\uFe0F\u20E3"
                    targets[f"{reaction_template}"] = player.user
                    target_string += f"{reaction_template} : {str(player.user)}"
                    # targets.append(reaction_template)
                    i += 1
                target_embed = new_embed("COUP - Select a target!",target_string)
                target_message = await discord_integration.DM_no_response(ctx,self.user,None,target_embed)
                for key in targets.keys():
                    await target_message.add_reaction(key) # This may not work, may have to hard-code the emojis

                chosen_target = await discord_integration.wait_for_reaction(ctx,targets.keys(),self.user,dm_channel)
                target = targets[str(chosen_target)]

            """HANDLE CHALLENGE HERE"""
            challenged = False
            if reactions[str(choice)].__name__.replace("_"," ").lower().strip() in ['tax','assassinate','steal','exchange']:
                e = new_embed("COUP - Challenge",f"If you wish to challenge please react to this message. You have **10** seconds to do so.")
                msg = await discord_integration.send_message(ctx,None,e)
                await discord_integration.add_reaction_(ctx,msg,'⚠️',None)
                    
            users = player_list
            users.remove(self)
            reaction = await discord_integration.wait_for_reaction_timeout_global(ctx,['⚠️'],users,[ctx.channel],10)
            if reaction:
                def has_correct_card():
                    name = reactions[str(choice)].__name__.replace("_"," ")
                    if name == "tax" and 'duke' in self.cards:
                        return True
                    elif name == "steal" and 'captain' in self.cards:
                        return True
                    elif name == "assassinate" and 'assassin' in self.cards:
                        return True
                    elif name == 'exchange' and 'ambassador' in self.cards:
                        return True
                    else:
                        return False
                    
                def GetShowCard():
                    name = reactions[str(choice)].__name__.replace("_"," ")
                    if name == "tax" and 'duke' in self.cards:
                        return 'duke'
                    elif name == "steal" and 'captain' in self.cards:
                        return 'captain'
                    elif name == "assassinate" and 'assassin' in self.cards:
                        return 'assassin'
                    elif name == 'exchange' and 'ambassador' in self.cards:
                        return 'ambassador'
                    else:
                        return 'An unknown error occured'
                
                prompt = f"{'have the correct card to perform your action. React with ⚠️ to show the card and win the challenge. Do nothing and you lose the challenge and an influence.' if has_correct_card() else 'do not have the correct card to perform your action. You lose the challenge!'}"
                e = new_embed("COUP - Action challenged!",f"{str(self.user)} challenges your action. You {prompt}")
                e.add_field(name="\u2800",value="You have **10** seconds.",inline=False)
                msg = await discord_integration.DM_no_response(ctx,self.user,None,e)
                if has_correct_card():
                    await discord_integration.add_reaction_(ctx,msg,'⚠️',None)
                    reaction = await discord_integration.wait_for_reaction(ctx,['⚠️'],self.user,dm_channel,10)
                    if reaction:
                        #Show the card to everyone, and prompt user for if they should switch out the card
                        e = new_embed("COUP - Challenge",f"{str(self.user)} wins the challenge by showing their {GetShowCard()}. Awaiting response...")
                        await discord_integration.send_message(ctx,None,e)
                        e = new_embed("COUP - Replace?",f"Do you wish to replace your {GetShowCard()}?\nReact with ⚠️ to replace the card with a random card from the deck.\nYou have **10** seconds!")
                        msg = await discord_integration.DM_no_response(ctx,self.user,None,e)
                        await discord_integration.add_reaction_(ctx,msg,'⚠️',None)
                        reaction = await discord_integration.wait_for_reaction(ctx,['⚠️'],self.user,dm_channel,10)
                        if reaction:
                            #Replace the card
                            old_card = GetShowCard()
                            self.cards.remove(old_card)
                            deck.add_card(old_card)
                            deck.shuffle()
                            new_card = deck.draw_card()
                            self.cards.append(new_card)
                    else:
                        self.eliminate(ctx=ctx,deck=deck,target=target,player_list=player_list)
                        challenged = True
                else:
                    self.eliminate(ctx=ctx,deck=deck,target=target,player_list=player_list)
                    challenged = True
            if challenged == False:
                reactions[str(choice)](ctx=ctx,deck=deck,target=target,player_list=player_list)
        name = None
        try:
            name = reactions[str(choice)].__name__.replace("_"," ")
        except:
            pass
        return {
            'action': name or 'block',
            'on':(f' on {target}' if target != None else '')
        }

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
            self.cards.append(x.lower())

    def add_card(self,card):
        self.cards.append(card)

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
    TIME_IN_SECONDS = 60

    e = new_embed('COUP',f"React with 👍 to join the game of coup!\nA maximum of {MAX_PLAYERS} players can join! ({len(REACTIONS)}/{MAX_PLAYERS})\nYou have **{TIME_IN_SECONDS}** seconds left to react!")
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
            e.description = f"React with 👍 to join the game of coup!\nA maximum of {MAX_PLAYERS} players can join! ({len(REACTIONS)}/{MAX_PLAYERS})\nYou have **{int(TIME_IN_SECONDS-((x/MULTIPLIER)+1))}** seconds left to react!"
            await message.edit(embed=e)

    players = []
    for value in REACTIONS:
        players.append(Player(value['user']))
    await message.delete()
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
    for player in players:
        if player.cards == []:
            player.cards.append(d.draw_card())
            player.cards.append(d.draw_card())
    if len(players) < 2:
        e = new_embed("COUP","Sorry, not enough players joined!")
        GAME_IN_PROGRESS = False
        START_CHECK = False
        STARTED_BY_ID = None
        event.USER_REACTED.remove_handler(reaction_handle)
        event.USER_UNREACTED.remove_handler(unreaction_handle)
        await ctx.send(embed=e)
        return

    GAME_STAGE = 2   
    
    #Shuffle the deck
    d.shuffle()

    async def TakeTurn(player):
        action = await player.MakeAction(ctx, players, d) ################################################################### NOT COMPLETED ################################################################################
        return action

    for player in players:
        e = new_embed("COUP - Your cards",f"{player.cards[0]}: {characters[player.cards[0]]}\n{player.cards[1]}: {characters[player.cards[1]]}")
        await discord_integration.DM_no_response(ctx,player.user,None,e)
    
    # define the main game loop
    current_player = 0
    while len(players) > 1:
        player = players[current_player]
        result = await TakeTurn(player)
        action = result['action']
        on = result['on']
        success = f"{player} successfully chose to use {action}{on}"
        fail = f"{player} failed to use {action}{on}"
        e = new_embed("COUP",(success if result != 'block' else fail))
        await ctx.send(embed=e)
        current_player = (current_player + 1) % len(players)
        while player.dead:
            players.remove(current_player)
            player = (current_player + 1) % len(players)

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




"""

e = new_embed("COUP - Block","React with 🛡️ to block the action.")
    player_list = kwargs['player_list']
    ctx = kwargs['ctx']
    for player in player_list:
        msg = await discord_integration.DM_no_response(ctx,player.user,None,e)
        await discord_integration.add_reaction_(ctx,msg,"🛡️",None)
    reaction = discord_integration.wait_for_reaction_timeout(ctx,["🛡️"],[player.user for player in player_list])
    if reaction != None:
        # Blocked, does self challenge the block?
        user = await ctx.bot.fetch_user(reaction.user_id)
        e = new_embed("COUP - Blocked",f"{str(user)} has blocked {str(self.user)} from using foreign aid. Waiting for response about challenging the block...")
        await discord_integration.send_message(ctx,None,e)
        e = new_embed("COUP - Action blocked",f"{str(user)} has blocked your foreign aid. Do you challenge the block? (You have 10 seconds to decide)\nReact with ⚠️ to challenge. Do nothing and the block is automatically successful")
        msg = await discord_integration.DM_no_response(ctx,self.user,None,e)
        await discord_integration.add_reaction_("⚠️")
        reaction = await discord_integration.wait_for_reaction_timeout(ctx,['⚠️'],[self.user],10)
        if reaction:
            #Challenged
            e = new_embed("COUP - Block challenged!",f"{str(self.user)} challenges {str(user)}'s block. Awaiting response...")
            await discord_integration.send_message(ctx,None,e)
            def has_correct_card_to_block():
                return 'duke' in self.cards
                
            prompt = f"{'have the correct card to block. React with any reaction to show the card and win the challenge. Do nothing and you lose the challenge and an influence.' if has_correct_card_to_block() else 'do not have the correct card to block. You lose the challenge!'}"
            e = new_embed("COUP - Block challenged!",f"{str(self.user)} challenges your block. You {prompt}")
            msg = await discord_integration.DM_no_response(ctx,user,None,e)
        else:
            #Block successful
            #ACTION
    else:
        #ACTION
"""