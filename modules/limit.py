import discord
import sqlite3
from discord.ext import commands

from v import LIMIT


class Limit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def limit(self, ctx, limit: int):

        author = ctx.author
        guild = ctx.guild

        db = sqlite3.connect('voice.db')    
        cur = db.cursor()   

        cur.execute(f"SELECT * FROM User WHERE userID = {author.id} AND guildID = {guild.id}")
        data = cur.fetchone()

        if data:

            user_channel = guild.get_channel(data[3])
                    
            if limit <= 99 and limit >= 1:

                await user_channel.edit(user_limit=limit) 
                await ctx.send(f"{author.mention} {LIMIT} Voice chat limit changed to `{limit}`")

            else:
                await ctx.send(f"{author.mention} - Please set a limit less than `100` and greater than `1`. You entered `{limit}`")

        else:
            await ctx.send(f"{author.mention} - You do not have an ongoing voice chat!")

            
def setup(bot):
    bot.add_cog(Limit(bot))
