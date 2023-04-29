import discord

async def DM_with_response(ctx, user=None, prompt=None, embed=None, whitelist=[], check=None):
    assert isinstance(embed, discord.Embed) or embed == None, f"Embed must be of type 'discord.Embed' or 'None', not {type(embed)}"
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




async def DM_no_response(ctx, user=None, prompt=None, embed=None):
    assert isinstance(embed, discord.Embed) or embed == None, f"Embed must be of type 'discord.Embed' or 'None', not {type(embed)}"
    assert ctx != None, "Missing required CONTEXT object"
    message = await user.send(content=prompt, embed=embed)
    def check_for_user(message):
        return message.author.id == user.id
    response = await ctx.bot.wait_for('message', check=check_for_user, timeout=None)
    return response




async def send_message(ctx, prompt=None, embed=None):
    assert isinstance(embed, discord.Embed) or embed == None, f"Embed must be of type discord.Embed"
    assert ctx != None, "Missing required CONTEXT object"
    message = await ctx.send(content=prompt, embed=embed)
    return message


"""
ctx : Discord context object
str_reactions : a list of reaction emojis in string form
user : discord.User object
channel : A discord channel object.
"""
async def wait_for_reaction(ctx, str_reactions, user, channel, timeout=None):
    assert isinstance(user, discord.User), "user must be of type discord.User"
    assert channel != None, "Channel cannot be None, must have channel value"
    
    def check(reaction, reacting_user):
        return str(reaction.emoji) in str_reactions and reacting_user == user and reaction.message.channel == channel

    try:
        reaction, _ = await ctx.bot.wait_for('reaction_add', check=check, timeout=timeout)
    except Exception:
        return None
    else:
        return reaction

async def wait_for_reaction_timeout(ctx, str_reactions, user_list, timeout=None):    
    def check(reaction, reacting_user):
        return str(reaction.emoji) in str_reactions and reacting_user in user_list and reaction.message.channel in [user.create_dm() for user in user_list]

    try:
        reaction, _ = await ctx.bot.wait_for('reaction_add', check=check, timeout=timeout)
    except Exception:
        return None
    else:
        return reaction

async def add_reaction(ctx, message, reaction=None, reaction_id=None):
    assert ctx != None, "Missing required CONTEXT object"
    assert message != None, "Missing required discord.Message object"
    assert reaction != None or reaction_id != None, "Requires either reaction or reaction id, both appear to be 'None'"
    final_reaction = reaction
    if final_reaction == None:
        final_reaction = ctx.bot.get_emoji(reaction_id)
    await message.add_reaction(final_reaction)




async def remove_reaction(message, reaction):
    assert message != None, "Missing required discord.Message object"
    await message.clear_reaction(reaction)




async def edit_message(message, new_content=None, new_embed=None):
    assert message != None, "Missing required discord.Message object"
    return await message.edit(content=new_content,embed=new_embed)