import os
import random

"""
TODO:
    - Complete GetPlayers() function
    - Complete game logic loop
    - Complete the Deck class
"""

description = """WIP."""

class Player:
    def __init__(self, user):
        self.user = user
        self.cards = []

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
            pass

"""
Creates a 'join prompt' in the server's channel that this was sent from.
Requires reaction to join, unreact to un-join
"""
async def GetPlayers():
    #Requires Player object
    pass

async def run(ctx, *args):
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN
    characters = {
        'Duke': 'Tax (Take 3 coins from the treasury)',
        'Assassin': 'Assassinate (Pay 3 coins to eliminate a player\'s influence)',
        'Captain': 'Steal (Take 2 coins from another player)',
        'Ambassador': 'Exchange (Trade in 2 cards from the deck)',
        'Contessa': 'Block (Block an assassination attempt)',
    }

    d = Deck()
    d.refresh(characters=characters)

    #Get players
    players = await GetPlayers()

    #Set coins
    coins = {player: 2 for player in players} #start with 2 coins

    #Set influence
    influence = {player: 2 for player in players}
    
    

    #Shuffle the deck
    d.shuffle()

    def tax(player):
        coins[player] += 3

    def eliminate(player):
        influence[player] -= 1
        if influence[player] == 0:
            players.remove(player)

    def assassinate(player, target):
        if coins[player] >= 3:
            coins[player] -= 3
            eliminate(target)

    def steal(player, target):
        if coins[target] >= 2:
            coins[player] += 2
            coins[target] -= 2

    def exchange(player):
        cards = d.draw_cards(2)
        # let the player choose which cards to keep
        # and which to return to the deck

    def block(player):
        pass # blocking an assassination attempt is automatic

    async def TakeTurn(player):
        pass

    # define the main game loop
    current_player = 0
    while len(players) > 1:
        player = players[current_player]
        result = await TakeTurn(player)
        await ctx.send(f"{player} chose to {result}")
        current_player = (current_player + 1) % len(players)

    # determine the winner
    if len(players) == 1:
        print(f"{players[0]} wins!")
    else:
        print("It's a tie!")