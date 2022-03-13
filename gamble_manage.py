import discord
import datetime
import pickle
import os
import json
from discord.ext import commands

with open(os.path.join("info", 'setting.json'),'r',encoding='utf8')as jfile:
    jdata = json.load(jfile)

# commands for guild manager
class gamble_management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.gamble_info = {} 

    # check if command user have enough permission
    async def have_permission(self, author_id):
        # put manager's user id in list manager_id
        manager_id = []
        return author_id in manager_id 

    # give target member certain amount of money, value can be negative
    @commands.command(hidden = True)
    async def give(self, ctx, target_ment:str, amount:int = 0):
        # check if command user have permission
        if not (await self.have_permission(ctx.author.id)):
            await ctx.send('you have no permission to use this command')
            return

        with open(os.path.join("info", 'gamble_info'), 'rb') as f:
            self.gamble_info = pickle.load(f)

        # variables for later
        target_id = int(target_ment[3:-1])
        target_pos = self.gamble_info[ctx.guild.id][2].index(target_id)
        name = "**" + self.gamble_info[ctx.guild.id][1][target_pos] + "**"

        # edit and update data
        if target_id in self.gamble_info[ctx.guild.id][2]:
            self.gamble_info[ctx.guild.id][3][target_pos] += amount
            embed = discord.Embed(description = "已給予 %s %i%s" %(name, amount, ":shrimp:"), color = 0x11df60)
            await ctx.send(embed = embed)
        else:
            await ctx.send("target info doesn't exist")
            pass

        with open(os.path.join("info", 'gamble_info'), 'wb') as f:
            pickle.dump(self.gamble_info, f)

    # command to show the file with member info and detail
    @commands.command(hidden = True)
    async def showfile(self, ctx):
        # check if command user have permission
        if not (await self.have_permission(ctx.author.id)):
            await ctx.send('you have no permission to use this command')
            return

        with open(os.path.join("info", 'gamble_info'), 'rb') as f:
            self.gamble_info = pickle.load(f)
        await ctx.send(self.gamble_info[ctx.guild.id])

    # clear target member's cooldown of command the ;timely
    @commands.command(hidden = True)
    async def clear_cooldown(self, ctx, target_ment:str):
        # check if command user have permission
        if not (await self.have_permission(ctx.author.id)):
            await ctx.send('you have no permission to use this command')
            return

        with open(os.path.join("info", 'gamble_info'), 'rb') as f:
            self.gamble_info = pickle.load(f)

        target_id = int(target_ment[3:-1])

        if target_id in self.gamble_info[ctx.guild.id][2]:
            pos = self.gamble_info[ctx.guild.id][2].index(target_id)
            self.gamble_info[ctx.guild.id][4][pos] = datetime.datetime.now()
            await ctx.send("cooldown refreshed")
        else:
            ctx.send("target info doesn't exist")
            pass

        with open(os.path.join("info", 'gamble_info'), 'wb') as f:
            pickle.dump(self.gamble_info, f)

    # delete file
    @commands.command(hidden = True)
    async def delete_file(self, ctx):
        if not (await self.have_permission(ctx.author.id)):
            await ctx.send('you have no permission to use this command')
            return

        if not os.path.isfile("info/gamble_info"):
            print("file doesn't exist")
            pass
        else:
            os.remove("info/gamble_info")
            print("gamble_info removed secessfully")
            print(self.gamble_info)
            
def setup(bot):
    bot.add_cog(gamble_management(bot))
