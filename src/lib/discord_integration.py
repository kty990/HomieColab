import discord

async def DM_with_response(ctx, user=None, prompt=None, embed=None, whitelist=[], check=None):
    assert check != None, "Must have a 'check' function to use discord_integration.DM_with_response"
    assert ctx != None, "Missing required CONTEXT object"
    whitelisted = True
    if whitelist == []:
        whitelisted = False
    
    message = await user.send(content=prompt, embed=embed)
    response = await ctx.bot.wait_for('message', check=check, timeout=None)
    if whitelisted:
        while response.content.lower() not in [str(x).lower() for x in whitelist]:
            tmp = '\n'.join(whitelist)
            await user.send(f"That is not an acceptable response. Please choose from one of the following responses:\n{tmp}")
            response = await ctx.bot.wait_for('message', check=check, timeout=None)
    return response.content

async def send_message(ctx, prompt=None, embed=None):
    assert ctx != None, "Missing required CONTEXT object"
    message = await ctx.send(content=prompt, embed=embed)
    return message

async def add_reaction(ctx, message, reaction=None, reaction_id=None):
    final_reaction = reaction
    if final_reaction == None:
        final_reaction = ctx.bot.get_emoji(reaction_id)
    await message.add_reaction(final_reaction)

async def remove_reaction(message, reaction):
    await message.clear_reaction(reaction)