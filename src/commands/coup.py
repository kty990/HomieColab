import os
current_file = os.path.basename(__file__)
def run(ctx):
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN
    ctx.send("this is placeholder text for the %s command" % (str(current_file).replace(".py","")))
    #step 1 initialize game

    #step 2 get the number of players in the game by reacting to whatever gets spit out once a game is initialized 

    #step 3 star the game with another reaction on the thing that gets spit out

    #step 4 DM's all players that reacted what cards they have and probably says a little description of what they can do

    #step 5 randomly picks player order

    #step 6 starts game, spits out what the player can do with reactions

    #step 7 there is an objection thingy I suppose after the players action

    #step 8 challenge the objection or accept the objection

    #repeat until winner?