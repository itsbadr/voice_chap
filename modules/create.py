import discord
import asyncio
import sqlite3
from discord.ext import commands

from v import CREATE, PEN, COG, VOICE, get_prefix


class Create(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    def get_channel(self, m, server):
                
        if m.channel_mentions:

            return m.channel_mentions[0]
                
        if m.content:
                    
            text = m.content.split()[0]

            channel = discord.utils.get(server.guild.channels, name=text)

            return channel
        
        return None


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def create(self, ctx):

        p = get_prefix(self.bot, ctx)

        guild = ctx.guild
        author = ctx.author

        db = sqlite3.connect('voice.db')    
        cur = db.cursor()

        cur.execute(f"SELECT guildID FROM Guild WHERE guildID = {guild.id}")
            

        if cur.fetchone() is None:
            
            def check(m):
                return m.author == author and m.guild == guild

            await ctx.send(f"{author.mention} {CREATE} What will your category name be?")

            try:
                category_name = await self.bot.wait_for('message', check=check, timeout=60.0)

            except asyncio.TimeoutError:
                await ctx.send(f"Took too long to enter! Restart by typing `{p}create`")
                
            else:
                await ctx.send(f"{author.mention} {PEN} What will your voice chat name be?")

                try:
                    channel_name = await self.bot.wait_for('message', check=check, timeout = 60.0)

                except asyncio.TimeoutError:
                        await ctx.send(f"{author.mention} - Took too long to enter! Restart by typing `{p}create`")

                else:
                    await ctx.send(f"{author.mention} {COG} Where would you like to send the settings messages?\n"
                                                        "Set this to a channel where you usually use your bots!")
                    try:
                        settings_message = await self.bot.wait_for('message', check=check, timeout = 60.0)

                    except asyncio.TimeoutError:
                            await ctx.send(f"{author.mention} - Took too long to enter! Restart by typing `{p}create`")

                    else:

                        settings_channel = self.get_channel(settings_message, ctx)

                        if settings_channel is None:
                            await ctx.send(f"{ctx.author.mention} - Channel with name `{settings_message.content}` does not exist!")

                        else:
                            category = await guild.create_category_channel(category_name.content)

                            channel = await category.create_voice_channel(channel_name.content)

                            settings = await category.create_voice_channel("Settings")

                            await settings.set_permissions(self.bot.user, connect=True, read_messages=True)

                            await settings.set_permissions(guild.default_role, connect=False)

                            cur.execute("INSERT INTO Guild VALUES (?, ?, ?, ?, ?, ?, ?)",
                             
                            (guild.id,
                            guild.name,
                            channel.id,
                            channel.name,
                            settings.id,
                            settings_channel.id,
                            category.id))

                            db.commit()

                            await ctx.send(f"{author.mention} {VOICE} Your server has been set up and the channels are ready to use!\n"
                                            f"To get started, type `{p}help`!")
        else:
            await ctx.send("Already exists.")
    
    @create.error
    async def create_error(self, ctx, error):

        print(error)
            
            
def setup(bot):
    bot.add_cog(Create(bot))
