import discord
import sqlite3
from discord.ext import commands

class LeaveEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        guild = member.guild

        db = sqlite3.connect('voice.db')
        cur = db.cursor()

        cur.execute(f"SELECT * FROM User WHERE userID = {member.id}")

        data = cur.fetchone()

        if data is None:
            return

        else:

            user_channel = guild.get_channel(data[3])

            await user_channel.delete()

            cur.execute(f"DELETE FROM User WHERE userID = {member.id}")

            db.commit()


                

def setup(bot):
    bot.add_cog(LeaveEvent(bot))
