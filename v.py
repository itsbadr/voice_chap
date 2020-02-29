import discord
import asyncio
import sqlite3
import json
import os
from discord.ext import commands

def get_prefix(bot, context):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    try:
        prefixes[str(context.guild.id)]
    except KeyError:
        return "."

    return prefixes[str(context.guild.id)]
    

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')

token = ''

PEN = '<a:pencilgif:673604442817298483> '
LIMIT = '<a:limitgif:673616027539472410> '
DELETE = '<a:deletegif:673601274784120833> '
COG = '<a:coggif:673607002248839198> '
CREATE = '<a:creategif:673617825184612352>'
RESET = '<:reset:673482739621691392>'
TRANSPARENT = '<:transparent:673481153411416074>'
VOICE = '<a:speakergif:673900266843799572>'
PREFIX = '<a:prefixgif:674589910870786049>'

@bot.event
async def on_ready():

    print(f"Online")

@bot.command()
async def help(ctx):

    p = get_prefix(bot, ctx)

    embed = discord.Embed(color=0x7c7be3,
                          description=
                                      f"{PEN}{TRANSPARENT}**NAME** -  "
                                      f"Type `{p}name (name)` to set your voice chat name\n\n"

                                      f"{LIMIT}{TRANSPARENT}**LIMIT** - "
                                      f"Type `{p}limit (number)` to set your voice chat limit\n\n"

                                      f"{DELETE}{TRANSPARENT}**DELETE** - "
                                      f"Type `{p}delete` to delete your voice chat\n\n"

                                      f"{COG}{TRANSPARENT}**SETUP (FOR MODS ONLY)**{TRANSPARENT}{COG}\n\n"

                                      f"{VOICE}{TRANSPARENT}**CREATE** - "
                                      f"Type `{p}create` to set up everything\n\n"

                                      f"{RESET}{TRANSPARENT}**RESET** - "
                                      f"Something went wrong? Type `{p}reset` to reset and start over\n\n"

                                      f"{PREFIX}{TRANSPARENT}**PREFIX** - "
                                      f"Type `{p}prefix (prefix)` to set a different prefix!"
                        )
    embed.set_footer(text="For settings, join the Settings voice chat")

    embed.set_author(name=f"VoiceChap Commands", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def prefix(ctx, prefix):

    with open('signs.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(ctx.guild.id)] = prefix

    with open('signs.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

    await ctx.send(f"{ctx.author.mention} {PREFIX} Prefix set to `{prefix}`")

@bot.event
async def on_command_error(_, error):

    if isinstance(error, commands.CommandNotFound):
        return

for filename in os.listdir('./modules'):
    
    if filename.endswith('.py'):
        bot.load_extension(f'modules.{filename[:-3]}')
        print(f"{filename} loaded.")


bot.run(token)
