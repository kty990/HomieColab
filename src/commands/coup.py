import os
import random

"""
TODO:
    - Complete GetPlayers() function
    - Complete game logic loop
    - Complete the Deck class
"""

description = """WIP."""

class Deck:
    def __init__(self):
        self.cards = []
    
    def shuffle():
        pass

    def draw_cards(num):
        pass

    def draw_card():
        pass

async def GetPlayers():
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

    NUM_OF_CARD_IN_DECK = 3
    d = Deck()

    #Get players
    players = await GetPlayers()

    #Set coins
    coins = {player: 2 for player in players} #start with 2 coins

    #Set influence
    influence = {player: 2 for player in players}
    
    #Populate deck
    for x in list(characters.keys()) * NUM_OF_CARD_IN_DECK:
        pass

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

    # define the main game loop
    current_player = 0
    while len(players) > 1:
        player = players[current_player]
        # GAME LOGIC HERE
        current_player = (current_player + 1) % len(players)

    # determine the winner
    if len(players) == 1:
        print(f"{players[0]} wins!")
    else:
        print("It's a tie!")