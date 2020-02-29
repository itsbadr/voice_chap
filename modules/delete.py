import discord
import sqlite3
from discord.ext import commands

from v import DELETE


class Delete(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['destroy', 'fuckoff', 'kill', 'yeet'])
    async def delete(self, ctx):

        author = ctx.author
        guild = ctx.guild

        db = sqlite3.connect('voice.db')    
        cur = db.cursor()

        cur.execute(f"SELECT * FROM Guild WHERE guildID = {guild.id}")
        guild_data = cur.fetchone()

        cur.execute(f"SELECT * FROM User WHERE userID = {author.id} AND guildID = {guild.id}")
        data = cur.fetchone()
 
        if guild_data:

            if data:

                user_channel = guild.get_channel(data[3])
                await user_channel.delete()

                voice_channel = guild.get_channel(guild_data[2])
                await voice_channel.set_permissions(author, overwrite=None)

                settings_channel = guild.get_channel(guild_data[4])                   
                await settings_channel.set_permissions(author, overwrite=None)

                cur.execute(f"DELETE FROM User WHERE userID = {author.id} AND guildID = {guild.id}")
                db.commit()

                await ctx.send(f"{author.mention} {DELETE} Your voice channel was deleted!")
            
            else:
                await ctx.send(f"{author.mention} - You do not have an ongoing voice chat!")
        
        else:
            return
            

def setup(bot):
    bot.add_cog(Delete(bot))
