import os

async def run(ctx, *args):
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN
    pass
    
    



















#EXAMPLE GAME LOOP FOR A GAME OF COUP
"""



import random

# define the characters and their abilities
characters = {
    'Duke': 'Tax (Take 3 coins from the treasury)',
    'Assassin': 'Assassinate (Pay 3 coins to eliminate a player\'s influence)',
    'Captain': 'Steal (Take 2 coins from another player)',
    'Ambassador': 'Exchange (Trade in 2 cards from the deck)',
    'Contessa': 'Block (Block an assassination attempt)',
}

# initialize the game variables
players = ['Player 1', 'Player 2', 'Player 3']
influence = {player: 2 for player in players}
coins = {player: 2 for player in players}
deck = list(characters.keys()) * 3
random.shuffle(deck)

# define the functions for the character actions
def tax(player):
    coins[player] += 3

def assassinate(player, target):
    if coins[player] >= 3:
        coins[player] -= 3
        eliminate(target)

def steal(player, target):
    if coins[target] >= 2:
        coins[player] += 2
        coins[target] -= 2

def exchange(player):
    cards = draw_cards(2)
    # let the player choose which cards to keep
    # and which to return to the deck

def block(player):
    pass # blocking an assassination attempt is automatic

# define the functions for drawing and eliminating cards
def draw_card():
    if len(deck) == 0:
        shuffle_deck()
    return deck.pop()

def draw_cards(num):
    return [draw_card() for _ in range(num)]

def eliminate(player):
    influence[player] -= 1
    if influence[player] == 0:
        players.remove(player)

# define the main game loop
current_player = 0
while len(players) > 1:
    player = players[current_player]
    action = input(f"{player}, choose an action: ")
    if action == 'Tax':
        tax(player)
    elif action == 'Assassinate':
        target = input(f"{player}, choose a target: ")
        assassinate(player, target)
    # similar elif statements for the other actions
    else:
        print("Invalid action. Try again.")
        continue
    current_player = (current_player + 1) % len(players)

# determine the winner
if len(players) == 1:
    print(f"{players[0]} wins!")
else:
    print("It's a tie!")


    
    
    
    """