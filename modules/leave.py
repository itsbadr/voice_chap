import discord
import sqlite3
from discord.ext import commands

class Leave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if before.channel:

            guild = member.guild

            db = sqlite3.connect('voice.db')
            cur = db.cursor()

            cur.execute(f"SELECT * FROM User WHERE channelID = {before.channel.id}")

            data = cur.fetchone()

            if data is None:
                return

            else:

                user = guild.get_member(data[1])

                user_channel = guild.get_channel(data[3])

                cur.execute(f"SELECT * FROM Guild WHERE guildID = {guild.id}")

                data = cur.fetchone()

                voice_channel = guild.get_channel(data[2])

                settings_channel = guild.get_channel(data[4])           

                if user_channel is None:
                    return
                
                else:

                    if before.channel.id == user_channel.id and len(before.channel.members) <= 0:
                        
                        if user in settings_channel.members:
                            return

                        else:
                        
                            await voice_channel.set_permissions(user, overwrite=None)
                            
                            await settings_channel.set_permissions(user, overwrite=None)

                            await before.channel.delete()

                            cur.execute(f"DELETE FROM User WHERE userID = {user.id} AND guildID = {guild.id}")
                            db.commit()

                    else:
                        return


def setup(bot):
    bot.add_cog(Leave(bot))
