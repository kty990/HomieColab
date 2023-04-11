import os
current_file = os.path.basename(__file__)
def run(ctx):
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN
    ctx.send("this is placeholder text for the %s command" % (str(current_file).replace(".py","")))