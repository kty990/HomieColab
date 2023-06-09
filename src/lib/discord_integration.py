import discord

async def DM_with_response(ctx, user=None, prompt=None, embed=None, whitelist=[], check=None):
    # assert isinstance(embed, discord.Embed) or embed == None, f"Embed must be of type 'discord.Embed' or 'None', not {type(embed)}"
    # assert check != None, "Must have a 'check' function to use discord_integration.DM_with_response"
    # assert ctx != None, "Missing required CONTEXT object"
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
    # assert isinstance(embed, discord.Embed) or embed == None, f"Embed must be of type 'discord.Embed' or 'None', not {type(embed)}"
    # assert ctx != None, "Missing required CONTEXT object"
    message = await user.send(content=prompt, embed=embed)
    return message




async def send_message(ctx, prompt=None, embed=None, file=None):
    # assert isinstance(embed, discord.Embed) or embed == None, f"Embed must be of type discord.Embed"
    # assert ctx != None, "Missing required CONTEXT object"
    message = await ctx.send(content=prompt, embed=embed, file=file)
    return message


"""
ctx : Discord context object
str_reactions : a list of reaction emojis in string form
user : discord.User object
channel : A discord channel object.
"""
async def wait_for_reaction(ctx, str_reactions, user, channel, timeout=None):
    # assert isinstance(user, discord.User), "user must be of type discord.User"
    # assert channel != None, "Channel cannot be None, must have channel value"
    
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

async def wait_for_reaction_timeout_global(ctx, str_reactions, user_list, channels, timeout=None):
    def check(reaction, reacting_user):
        return str(reaction.emoji) in str_reactions and reacting_user in user_list and reaction.message.channel in channels
    
    try:
        reaction, _ = await ctx.bot.wait_for('reaction_add', check=check, timeout=timeout)
    except Exception:
        return None
    else:
        return reaction
    
async def wait_for_reaction_all(ctx, msg, players, str_reactions):
    reactions = {}
    user_ids = [player.user.id for player in players]
    for user_id in user_ids:
        reaction, user = await ctx.bot.wait_for('reaction_add', check=lambda r, u: u.id == user_id and r.message.id == msg.id and str(r.emoji) in str_reactions)
        reactions[user_id] = reaction.emoji
    return reactions


async def add_reaction_(ctx, message, reaction=None, reaction_id=None):
    # assert ctx != None, "Missing required CONTEXT object"
    # assert message != None, "Missing required discord.Message object"
    # assert reaction != None or reaction_id != None, "Requires either reaction or reaction id, both appear to be 'None'"
    try:
        final_reaction = reaction
        if final_reaction == None:
            final_reaction = ctx.bot.get_emoji(reaction_id)
        print("Attempting reaction add")
        await message.add_reaction_(final_reaction)
        print("Reaction added!")
    except:
        pass

async def get_user_by_id(ctx, id):
    user = await ctx.bot.fetch_user(id)
    return user

async def get_emoji(ctx,reaction_id):
    return ctx.bot.get_emoji(reaction_id)

async def remove_reaction(message, reaction):
    # assert message != None, "Missing required discord.Message object"
    await message.clear_reaction(reaction)




async def edit_message(message, new_content=None, new_embed=None):
    # assert message != None, "Missing required discord.Message object"
    return await message.edit(content=new_content,embed=new_embed)