import discord
import sqlite3
from discord.ext import commands

class Join(commands.Cog):

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
        
                if after.channel.id == data[2]:

                    channel = after.channel
                    
                    user_channel = await channel.category.create_voice_channel(member.name)

                    await user_channel.set_permissions(self.bot.user, connect=True, read_messages=True)

                    await user_channel.set_permissions(member, connect=True)

                    await channel.set_permissions(member, connect=False)

                    settings_channel = guild.get_channel(data[4])
                    
                    await settings_channel.set_permissions(member, connect=True)

                    try:

                        await member.move_to(user_channel)
                    except:

                        await user_channel.delete()
                        await channel.set_permissions(member, overwrite=None)
                        await settings_channel.set_permissions(member, overwrite=None)

                    else:
                                 
                        cur.execute(f" INSERT INTO User VALUES (?, ?, ?, ?, ?, ?, ?) ",
                         
                        (guild.id, 
                        member.id, 
                        member.name, 
                        user_channel.id, 
                        user_channel.name, 
                        user_channel.user_limit, 
                        0))
                        
                        db.commit()


def setup(bot):
    bot.add_cog(Join(bot))
