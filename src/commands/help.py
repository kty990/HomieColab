import os
current_file = os.path.basename(__file__)
async def run(ctx):
    ### THIS IS EXECUTED WHEN THE COMMAND IS RUN
    await ctx.send("this is placeholder text for the %s command" % (str(current_file).replace(".py","")))