import discord
from discord.ext import commands
from discord.ext.commands import Greedy
from typing import Union

TOKEN = "token-here"

bot = commands.Bot(command_prefix='pls',
                   help_command=None,
                   activity=discord.Game(name="`pls yoink <emotes>` or `delete <emotes>`"),
                   strip_after_prefix=True)


@bot.event
async def on_ready():
    print('Ready!')


@commands.guild_only()
@bot.command(aliases=['add'])
async def yoink(ctx, emotes: Greedy[Union[discord.Emoji, discord.PartialEmoji]]):
    if not emotes:
        return await ctx.send('You didn\'t specify any emotes >:(')
    in_server, added = [], []
    for emote in emotes:
        if isinstance(emote, discord.Emoji) and emote.guild == ctx.guild:
            in_server.append(emote)
        else:
            added.append(await ctx.guild.create_custom_emoji(
                name=emote.name,
                image=await emote.url.read(),
                reason=f'Added by {ctx.author} ({ctx.author.id})'))

    if not added:
        return await ctx.send(f'Specified emote{"s" if len(emotes) != 1 else ""} are already in this server >:(')
    if in_server:
        return await ctx.send(f'{" ".join(map(str, added))} have been added to this server, while '
                              f'{" ".join(map(str, in_server))} wasn\'t because they are already added!')
    await ctx.send(f'{" ".join(map(str, added))} has been added to this server!')


@commands.is_owner()
@commands.guild_only()
@bot.command(aliases=['remove', 'del'])
async def delete(ctx, emotes: Greedy[discord.Emoji]):
    if not emotes:
        return await ctx.send('You didn\'t specify any emotes >:(')

    for emote in emotes:
        await emote.delete()
    await ctx.send(f'{len(emotes)} successfully deleted!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That\'s not a command >:(')
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send('You can\'t use that command in DM\'s >:(')


bot.run(TOKEN)
