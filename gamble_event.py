import discord
import os
import pickle
from discord.ext import commands

class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

        self.msgreact = {}

    # a command to add message id and it's corresponding role id to file
    @commands.command(hidden = True)
    async def add_msgreact(self, ctx, guild_id:int, msg_id:int, role_id:int):
        if os.path.isfile("info/gamble_msgreact"):
            pass
        else:
            with open(os.path.join( "info", 'gamble_msgreact'), 'wb') as f:
                pickle.dump(self.msgreact, f)

        print(guild_id)
        print(self.bot.get_guild(guild_id))
        guild_name = self.bot.get_guild(guild_id).name
        self.msgreact[guild_id] = {"guild_name":guild_name, 
         "reaction":{msg_id:role_id}}

        with open(os.path.join( "info", 'gamble_msgreact'), 'wb') as f:
            pickle.dump(self.msgreact, f)

    # commands for bot manager to monitor file
    @commands.command(hidden = True)
    async def show_msgreact_file(self, ctx):
        with open(os.path.join( "info", 'gamble_msgreact'), 'rb') as f:
            self.msgreact = pickle.load(f)

        await ctx.send(self.msgreact)

    # give guild member roles by adding reaction
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        with open(os.path.join( "info", 'gamble_msgreact'), 'rb') as f:
            self.msgreact = pickle.load(f)
        
        if not payload.guild_id in self.msgreact:
            return
        
        if not payload.message_id in self.msgreact[payload.guild_id]["reaction"]:
            return
        else:
            react_guild = self.bot.get_guild(payload.guild_id)
            react_role = react_guild.get_role(self.msgreact[payload.guild_id]["reaction"][payload.message_id])
            await payload.member.add_roles(react_role)
         
def setup(bot):
    bot.add_cog(event(bot))
