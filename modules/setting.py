import discord
import sqlite3
from discord.ext import commands

class Setting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel:

            guild = member.guild

            db = sqlite3.connect('voice.db')
            cur = db.cursor()

            cur.execute(f"SELECT * FROM Guild WHERE guildID = {guild.id}")

            data = cur.fetchone()

            if data is None:
                return

            else:

                if after.channel.id == data[4]:

                    cur.execute(f"SELECT channelID FROM User WHERE userID = {member.id} AND guildID = {guild.id}")

                    data = cur.fetchone()

                    if data:

                        user_channel = guild.get_channel(data[0])

                        await member.move_to(user_channel)


def setup(bot):
    bot.add_cog(Setting(bot))
