import discord
import sqlite3
from discord.ext import commands

from v import RESET, get_prefix


class Reset(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reset(self, ctx):

        p = get_prefix(self.bot, ctx)

        author = ctx.author
        guild = ctx.guild

        db = sqlite3.connect('voice.db')    
        cur = db.cursor()

        cur.execute(f"SELECT * FROM Guild WHERE guildID = {guild.id}")
        data = cur.fetchone()

        if data:

            category = guild.get_channel(data[6])
            
            if category is None:
                pass
            else:
                await category.delete()
            
            voice_channel = guild.get_channel(data[2])

            if voice_channel is None:
                pass
            else:
                await voice_channel.delete()
    
            settings_channel = guild.get_channel(data[4])
            
            if settings_channel is None:
                pass
            else:
                await settings_channel.delete()

            cur.execute(f"DELETE FROM Guild WHERE guildID = {guild.id}")
            db.commit()

            await ctx.send(f"{author.mention} {RESET} Your voice channels were reset! Type `{p}create` to start fresh")
        
        else:
            await ctx.send(f"{author.mention} - You have not yet setup the voice chats!")
            

def setup(bot):
    bot.add_cog(Reset(bot))
