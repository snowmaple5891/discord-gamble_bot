import asyncio
import pickle
import os
import json
from discord.ext import commands

with open(os.path.join( "info", 'setting.json'),'r',encoding='utf8')as jfile:
    jdata = json.load(jfile)

class gamble_examine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.gamble_info = {}   

    # check if gamble info exist
    async def if_file_exist(self, ctx):
        if not (os.path.isfile("info/gamble_info")):
            await ctx.send("尚未有任何資料")
            return True
        else:
            with open(os.path.join( "info", 'gamble_info'), 'rb') as f:
                self.gamble_info = pickle.load(f)
            return False

    # check if the player have enough mooney
    async def is_valid(self, ctx, member_id):
        with open(os.path.join( "info", 'gamble_info'), 'rb') as f:
            self.gamble_info = pickle.load(f)
    
        if member_id not in self.gamble_info[ctx.guild.id][2]:
            await ctx.send("您尚未領錢")
            return True

    # check if the bet is valid
    async def is_amount_valid(self, ctx, member_id, amount):  
        with open(os.path.join( "info", 'gamble_info'), 'rb') as f:
            self.gamble_info = pickle.load(f)
        pos = self.gamble_info[ctx.guild.id][2].index(member_id)
        if amount <= 0:
            await ctx.send('請輸入有效金額')
        elif amount > self.gamble_info[ctx.guild.id][3][pos]:
            await ctx.send('餘額不足')
        elif amount > 100000:
            await ctx.send('最大有效金額為100000')
        else:
            return False
        return True
            
def setup(bot):
    bot.add_cog(gamble_examine(bot))
