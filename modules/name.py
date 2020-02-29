import discord
import sqlite3
from discord.ext import commands

from v import PEN


class Name(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def name(self, ctx, *, name):

        author = ctx.author
        guild = ctx.guild

        db = sqlite3.connect('voice.db')    
        cur = db.cursor()

        cur.execute(f"SELECT * FROM User WHERE userID = {author.id} AND guildID = {guild.id}")
        data = cur.fetchone()

        if data:
            user_channel = guild.get_channel(data[3])
            await user_channel.edit(name=name) 

            await ctx.send(f"{author.mention} {PEN} Your voice channel name was changed to `{user_channel.name}`")
        
        else:
            await ctx.send(f"{author.mention} - You do not have an ongoing voice chat!")
            

def setup(bot):
    bot.add_cog(Name(bot))
