import sys
import os
import random
import asyncio
import copy
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib.embed import new_embed
from src.lib import discord_integration

prompts = [
    "You shouldn't do in public",
    "Things you wouldn't want to find in your bed",
    "Words to describe your private parts",
    "Types of people who should be sterilized",
    "Types of people who should be deported",
    "Ways to use a vibrator without it turning you on",
    "Things you wouldn't want to see your parents doing",
    "Things you shouldn't do with your partner's parents",
    "Ways to get out of a traffic ticket",
    "Things that can make you go blind",
    "Things you wouldn't want to find in your food",
    "Things you wouldn't want to do in a public restroom",
    "Things you wouldn't want to hear from your boss",
    "Things you shouldn't say to a police officer",
    "Things you shouldn't do during a job interview",
    "Things you shouldn't do on a first date",
    "Things you wouldn't want to hear from your gynecologist",
    "Things you wouldn't want to hear from your proctologist",
    "Things you wouldn't want to hear from your dentist",
    "Things you wouldn't want to hear from your accountant",
    "Things you wouldn't want to hear from your lawyer",
    "Things you wouldn't want to hear from your therapist",
    "Things you wouldn't want to hear from your mechanic",
    "Things you wouldn't want to hear from your hairdresser",
    "Things you wouldn't want to hear from your tattoo artist",
    "Things you wouldn't want to hear from your bartender",
    "Things you wouldn't want to hear from your flight attendant",
    "Things you wouldn't want to hear from your waiter",
    "Things you wouldn't want to hear from your landlord",
    "Things you wouldn't want to hear from your neighbor",
    "Things you wouldn't want to hear from your in-laws",
    "Things you wouldn't want to hear from your spouse",
    "Things you wouldn't want to hear from your child",
    "Things you wouldn't want to hear from your pet",
    "Things you wouldn't want to hear from your doctor",
    "Things you wouldn't want to hear from your nurse",
    "Things you wouldn't want to hear from your pharmacist",
    "Things you wouldn't want to hear from your teacher",
    "Things you wouldn't want to hear from your boss's boss",
    "Things you wouldn't want to hear on a first date",
    "Things you wouldn't want to find in your parents' bedroom",
    "Things you wouldn't want to hear from your parents about their sex life",
    "Things you wouldn't want to hear from your parents about their drug use",
    "Things you wouldn't want to hear from your therapist about your childhood",
    "Things you wouldn't want to hear from your partner about their ex",
    "Things you wouldn't want to hear from your partner about your ex",
    "Things you wouldn't want to hear from your partner about their sexual history",
    "Things you wouldn't want to hear from your partner about your sexual history",
    "Things you wouldn't want to find in your partner's browser history",
    "Things you wouldn't want to find in your partner's phone",
    "Things you wouldn't want to hear from your partner while having sex",
    "Things you wouldn't want to hear from your partner while cuddling",
    "Things you wouldn't want to hear from your partner while fighting",
    "Things you wouldn't want to hear from your partner's parents about your relationship",
    "Things you wouldn't want to hear from your partner's ex about your relationship",
    "Things you wouldn't want to hear from your partner's current lover about your relationship",
    "Things you wouldn't want to hear from your partner's previous lover about your relationship",
    "Things you wouldn't want to hear from your partner's therapist about your relationship",
    "Things you wouldn't want to hear from your partner's lawyer about your relationship",
    "Things you wouldn't want to hear from your partner's boss about your relationship",
    "Things you wouldn't want to hear from your partner's best friend about your relationship",
    "Things you wouldn't want to hear from your partner's worst enemy about your relationship",
    "Things you wouldn't want to hear from your partner's siblings about your relationship",
    "Things you wouldn't want to hear from your partner's children about your relationship",
    "Things you wouldn't want to hear from your partner's pets about your relationship",
    "Things you wouldn't want to hear from your partner's ex about your sex life",
    "Things you wouldn't want to hear from your partner's current lover about your sex life",
    "Things you wouldn't want to hear from your partner's previous lover about your sex life",
    "Things you wouldn't want to hear from your partner's therapist about your sex life",
    "Things you wouldn't want to hear from your partner's lawyer about your sex life",
    "Things you wouldn't want to hear from your partner's boss about your sex life",
    "Things you wouldn't want to hear from your partner's best friend about your sex life",
    "Things you wouldn't want to hear from your partner's worst enemy about your sex life",
    "Things you wouldn't want to hear from your partner's siblings about your sex life",
    "Things you wouldn't want to hear from your partner's children about your sex life",
    "Things you wouldn't want to hear from your partner's pets about your sex life",
    "Things you wouldn't want to hear from your partner's ex about your private parts",
    "Things you wouldn't want to hear from your partner's current lover about your private parts",
    "Things you wouldn't want to hear from your partner's previous lover about your private parts",
    "Things you wouldn't want to hear from your partner's therapist about your private parts",
    "Things you wouldn't want to hear from your partner's lawyer about your private parts",
    "Things you wouldn't want to hear from your partner's boss about your private parts",
    "Things you wouldn't want to hear from your partner's best friend about your private parts",
    "Things you wouldn't want to hear from your partner's worst enemy about your private parts",
    "Things you wouldn't want to hear from your partner's siblings about your private parts",
    "Things you wouldn't want to hear from your partner's children about your private parts",
    "Things you wouldn't want to hear from your partner's pets about your private parts",
    "Things you wouldn't want to hear from your therapist about your fantasies",
]

#Convert to lowercase
prompts = [x.lower() for x in prompts]

TESTING = True
description = """Five Second Rule: Uncensored. A game where you must say 3 things about a given category before 5 seconds elapses."""

class Player:
    def __init__(self, user):
        self.user = user
        self.score = 0

    def __repr__(self):
        return f"{self.user}"

class Deck:
    def __init__(self):
        self.cards = []
    
    def __repr__(self):
        return f"<Deck:{len(self.cards)} cards>"
    
    def shuffle(self):
        tmp = []
        for x in self.cards:
            tmp.append(self.cards.pop(random.randint(0,len(self.cards)-1)))
        self.cards = tmp

    def is_empty(self):
        return len(self.cards) == 0

    def draw_cards(self, num: int = 0):
        cards = []
        for _ in range(num):
            cards.append(self.cards.pop())
        return cards

    def draw_card(self):
        return self.cards.pop()
    
    def add_card(self,card):
        self.cards.append(card)
    
    def populate(self):
        #Populate deck
        for prompt in prompts:
            self.add_card(prompt)
        self.shuffle()

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
        return str(reaction.emoji) == "👍" and not user.bot

async def GetPlayers(ctx, MAX_PLAYERS):
    #Requires Player object
    global MESSAGE_ID,START_CHECK

    MULTIPLIER = 2
    TIME_IN_SECONDS = 60

    e = new_embed('Five Second Rule',f"React with 👍 to join the game of five second rule!\nA maximum of {MAX_PLAYERS} players can join! ({len(REACTIONS)}/{MAX_PLAYERS})\nYou have **{TIME_IN_SECONDS}** seconds left to react!")
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
            e.description = f"React with 👍 to join the game of five second rule!\nA maximum of {MAX_PLAYERS} players can join! ({len(REACTIONS)}/{MAX_PLAYERS})\nYou have **{int(TIME_IN_SECONDS-((x/MULTIPLIER)+1))}** seconds left to react!"
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
    global GAME_IN_PROGRESS, STARTED_BY_ID, START_CHECK
    print(args)
    TARGET_SCORE = 12
    try:
        if args[0].isdigit():
            TARGET_SCORE = int(args[0])
    except:
        pass
    
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
    players = await GetPlayers(ctx, 10)
    if len(players) < 2:
        e = new_embed("Five Second Rule!","Sorry, not enough players joined!")
        GAME_IN_PROGRESS = False
        START_CHECK = False
        STARTED_BY_ID = None
        event.USER_REACTED.remove_handler(reaction_handle)
        event.USER_UNREACTED.remove_handler(unreaction_handle)
        await discord_integration.send_message(ctx,None,e)
        return

    """ GAME LOGIC HERE """
    # define the main game loop
    current_player = 0
    while max([player.score for player in players]) != TARGET_SCORE:
        player = players[current_player]
        await discord_integration.send_message(ctx,f"NEW ROUND\n\nYou will have 3 seconds to read the card and then the timer will start.\n.")
        prompt = d.draw_card()
        e = new_embed("\u2800",f"**{prompt.upper()}**\n\n\u2800")
        msg = await discord_integration.send_message(ctx,f"{player.user.mention}",e)
        await asyncio.sleep(3)
        timer_e = new_embed("Timer",f"You have **{5}** seconds left.")
        timer = await discord_integration.send_message(ctx,None,timer_e)
        for x in range(1,6):
            await asyncio.sleep(1)
            timer_e.description = f"You have **{5-x}** seconds left."
            await discord_integration.edit_message(timer,None,timer_e)
        timer_e.description = f"Time's up!"
        await discord_integration.edit_message(timer,None,timer_e)
        x_emoji = await discord_integration.get_emoji(ctx,989702490209534004)
        e = new_embed(f"Five Second Rule! ({player})",f"React with ✅ if you believe they completed 3 related items, or {x_emoji} if you believe they did not.\n\nThe game will __not__ continue until all players have reacted.")
        msg = await discord_integration.send_message(ctx,None,e)
        await discord_integration.add_reaction_(ctx,msg,"✅")
        await discord_integration.add_reaction_(ctx,msg,x_emoji)

        def deepcopy(list):
            tmp = []
            for x in list:
                tmp.append(x)
            return tmp

        tmp = deepcopy(players)
        tmp.remove(player)

        results = []
        def action(**kwargs):
            reaction = kwargs['reaction']
            user = kwargs['user']
            if not reaction.emoji in ["✅",x_emoji]:
                print(f"{str(user)} reacted with {str(reaction)} but it doesn't seem valid... -fsr")
                return
            print(f"{str(user)} reacted with {str(reaction)} -fsr")
            for player in tmp:
                if player.user == user:
                    tmp.remove(player)
                    results.append(reaction.emoji)

        event.USER_REACTED.add_handler(action)
        while len(tmp) > 0:
            await asyncio.sleep(1)
        event.USER_REACTED.remove_handler(action)

        yay = 0
        nay = 0
        for value in results:
            if value == "✅":
                yay += 1
            else:
                nay += 1
        
        if yay > nay:
            player.score += 1
            scores = '\n'.join([f"{str(player.user)}: {player.score}" for player in players])
            e = new_embed(f"Five Second Rule! ({player})",f"Your prompt was voted as completed successfully!\nThe current scores are:\n{scores}")
            await discord_integration.send_message(ctx,None,e)
        else:
            scores = '\n'.join([f"{str(player.user)}: {player.score}" for player in players])
            e = new_embed(f"Five Second Rule! ({player})",f"Your prompt was voted as __not completed successfully__!\nThe current scores are:\n{scores}")
            await discord_integration.send_message(ctx,None,e)

        current_player = (current_player + 1) % len(players)

    # determine the winner
    result = sorted(players, key=lambda x: x.score, reverse=True)
    if len(result) == 2:
        result.append("n/a")
    e = new_embed("Five Second Rule! - Podium",f"🥇 - {result[0]}\n🥈 - {result[1]}\n🥉 - {result[2]}")
    await discord_integration.send_message(ctx,None,e)

    
    GAME_IN_PROGRESS = False
    START_CHECK = False
    STARTED_BY_ID = None
    event.USER_REACTED.remove_handler(reaction_handle)
    event.USER_UNREACTED.remove_handler(unreaction_handle)