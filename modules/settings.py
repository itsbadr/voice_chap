import sqlite3
import asyncio
import discord
from discord.ext import commands

NUMBER = {
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣',
    6: '6️⃣'
}

class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel:

            guild = member.guild

            settings = after.channel

            db = sqlite3.connect('voice.db')
            cur = db.cursor()

            cur.execute(f"SELECT * FROM Guild WHERE guildID = {guild.id}")

            data = cur.fetchone()

            if data is None:
                return

            else:

                delete_react = False

                settings_channel_send = guild.get_channel(data[5])
                
                if after.channel.id == data[4]:

                    cur.execute(f"SELECT * FROM User WHERE userID = {member.id} and guildID = {guild.id}")

                    data = cur.fetchone()

                    if data is None:
                        return
                    
                    else:

                        user_channel = guild.get_channel(data[3])
            
                        channel_locked = data[6]

                        await settings.set_permissions(member, connect=False)

                        embed = discord.Embed(title="Your voice chat settings:", color=0x85ff2b)

                        embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")

                        embed.add_field(name="**1️⃣  SET NAME**",
                                        value=f"Current VC name: `{user_channel.name}`. React to change",
                                        inline=False)

                        embed.add_field(name="**2️⃣  SET LIMIT**",
                                        value=f"Current limit: `{user_channel.user_limit}`. React to change",
                                        inline=False)

                        embed.add_field(name="**3️⃣  LOCK VC**",
                                        value=f"Current status: `{channel_locked}`. React to lock the VC",
                                        inline=False)

                        embed.add_field(name="**4️⃣  UNLOCK VC**",
                                        value=f"Current status: `{channel_locked}`. React to unlock the VC",
                                        inline=False)


                        embed.add_field(name="**5️⃣  DELETE VC**",
                                        value="React to delete the VC",
                                        inline=False)

                        message_settings = await settings_channel_send.send(member.mention, embed=embed)

                        def react_check(r, u):

                            return u == member and r.message.id == message_settings.id

                        for num, _ in enumerate(range(5), start=1):

                            await message_settings.add_reaction(str(NUMBER[num]))

                        try:

                            reaction, member = await self.bot.wait_for('reaction_add', timeout=30.0, check=react_check)

                            emoji = str(reaction.emoji)

                        except asyncio.TimeoutError:

                            await message_settings.clear_reactions()

                            await message_settings.edit(embed=embed.set_footer(text="Timed out!"))

                            if member in user_channel.members:

                                await settings.set_permissions(member, connect=True)
                            else:

                                await settings.set_permissions(member, overwrite=None)

                        else:

                            def check(m):
                                    return m.channel.id == settings_channel_send.id and m.author == member
                            
                            if emoji == '1️⃣':
                                
                                await settings_channel_send.send(f"{member.mention} - Type your new voice chat name:")

                                try:
                                    user_channel_name =  await self.bot.wait_for('message', timeout=15.0, check=check)

                                except asyncio.TimeoutError:
                                    await settings_channel_send.send(f"{member.mention} - Request timed out!")

                                else:

                                    try:
                                        await user_channel.edit(name=user_channel_name.content)
                                    except:
                                        return
                                    else:
                                        await settings_channel_send.send(f"{member.mention} - Your voice channel name was changed to `{user_channel.name}`")

                            elif emoji == '2️⃣':

                                await settings_channel_send.send(f"{member.mention} - Type your new voice chat limit:")

                                try:
                                    user_channel_limit =  await self.bot.wait_for('message', timeout=15.0, check=check)

                                except asyncio.TimeoutError:
                                    await settings_channel_send.send(f"{member.mention} - Request timed out!")
                                            
                                else:
                                    try:
                                        if int(user_channel_limit.content) <= 99:

                                            try:
                                                await user_channel.edit(user_limit=int(user_channel_limit.content))
                                            except:
                                                return
                                            else:
                                                await settings_channel_send.send(f"{member.mention} - Voice chat limit changed to `{user_channel_limit.content}`!")

                                        else:
                                            await settings_channel_send.send("Please enter a value less than 100!")

                                    except ValueError:
                                        await settings_channel_send.send("Please enter a number and not text!")
                            
                            elif emoji == '3️⃣':

                                try:
                                    await user_channel.set_permissions(member, connect=True)
                                    await user_channel.set_permissions(guild.default_role, connect=False)
                                except:
                                    return
                                else:
                                    await settings_channel_send.send(f"{member.mention} - Your voice channel is now locked!")

                            elif emoji == '4️⃣':

                                try:
                                    await user_channel.set_permissions(guild.default_role, overwrite=None)
                                    await user_channel.set_permissions(member, connect=True)
                                except:
                                    return
                                else:
                                    await settings_channel_send.send(f"{member.mention} - Your voice channel is now unlocked!")

                            elif emoji == '5️⃣':

                                delete_react = True

                                try:
                                    cur.execute(f"DELETE FROM User WHERE userID = {member.id} and guildID = {guild.id}")
                                    db.commit()
                                    await user_channel.delete()
                                except:
                                    return
                                else:
                                    cur.execute(f"SELECT channelID FROM Guild WHERE guildID = {guild.id}")
                                    data = cur.fetchone()

                                    channel = guild.get_channel(data[0])
                                    await channel.set_permissions(member, overwrite=None)
                                    await settings.set_permissions(member, overwrite=None)

                                    await settings_channel_send.send(f"{member.mention} - Your voice channel was deleted!")   

                            if delete_react:
                                await message_settings.clear_reactions()
                            else:
                                await settings.set_permissions(member, connect=True)
                                await message_settings.clear_reactions()
                            
                        
def setup(bot):
    bot.add_cog(Settings(bot))
