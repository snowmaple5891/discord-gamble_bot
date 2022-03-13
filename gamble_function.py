import discord
import pickle
import os
import json
import asyncio
from gamble_config import gamble_examine
from discord.ext import commands

with open(os.path.join("info", 'setting.json'),'r',encoding='utf8')as jfile:
    jdata = json.load(jfile)

class gamble_usage(commands.Cog):
    def __init__(self, bot, gamble_examine):
        self.gamble_examine = gamble_examine
        
        self.bot = bot 
        self.gamble_info = {}
        self.gamble_rank = {}
        self.gamble_shop = {}

    @commands.command()
    async def buy(self, ctx, num:int):
        if await gamble_examine.if_file_exist(self, ctx):
            return
        if await gamble_examine.is_valid(self, ctx, ctx.author.id):
            return
        if num-1 > len(list(self.gamble_shop.keys())):
            await ctx.send("merchandise doesn't exist")
            return
        with open(os.path.join("info", 'gamble_shop'), 'rb') as f:
            self.gamble_shop = pickle.load(f)

        pos = self.gamble_info[ctx.guild.id][2].index(ctx.author.id)
        merch_price = sorted(list(self.gamble_shop.keys()), reverse = True)[num-1]

        if self.gamble_info[ctx.guild.id][3][pos] < merch_price:
            await ctx.send('餘額不足')
            return
        else:
            self.gamble_info[ctx.guild.id][3][pos] -= merch_price
            embed = discord.Embed(description = "%s 已成功購買商品 #%i, 謝謝惠顧"%(self.gamble_info[ctx.guild.id][1][pos], num), color = 0x11df60)

        if num == 2:
            gamblegod_role = self.bot.get_guild(ctx.guild.id).get_role(int(jdata['gamblegod_role_id']))
            await ctx.author.add_roles(gamblegod_role)
            
        await ctx.send(embed = embed)
        await asyncio.sleep(0.75)
        await ctx.message.delete()

        with open(os.path.join("info", 'gamble_info'), 'wb') as f:
            pickle.dump(self.gamble_info, f)
    
    @commands.command(hidden = True)
    async def add_merch(self, ctx, merch_description, merch_value:int = 0):
        if not (os.path.isfile("info/gamble_shop")):
            await ctx.send("shop doesn't exist")
            return
        
        with open(os.path.join("info", 'gamble_shop'), 'rb') as f:
                self.gamble_shop = pickle.load(f)
        
        self.gamble_shop[merch_value] = merch_description

        with open(os.path.join("info", 'gamble_shop'), 'wb') as f:
            pickle.dump(self.gamble_shop, f)

        await ctx.send("%s added to shop sucessfully!"%merch_description)
        await asyncio.sleep(0.75)
        await ctx.message.delete()
    
    @commands.command(
        help = '''
        show shop detail, merchandise and price
        ''',
        brief = "show shop detail, merchandise and price"
    )
    async def shop(self, ctx):
        if not (os.path.isfile("info/gamble_shop")):
            with open(os.path.join("info", 'gamble_shop'), 'wb') as f:
                pickle.dump(self.gamble_shop, f)
        else:
            with open(os.path.join("info", 'gamble_shop'), 'rb') as f:
                self.gamble_shop = pickle.load(f)
        
        shop = discord.Embed(title = "商店", color = 0x11df60)
        value_hightolow = sorted(list(self.gamble_shop.keys()), reverse = True)

        count = 1

        for value in value_hightolow:
            if count > 9 : break
            shop.add_field(name = "#%s - "%count + str(value) + ":shrimp:", value = self.gamble_shop[value], inline = True)
            count += 1

        await ctx.send(embed = shop)
        await asyncio.sleep(0.75)
        await ctx.message.delete()
    
    @commands.command(
        help = '''
        show total currency rank in this guild
        ''',
        brief = "show total currency rank in this guild"
    )
    async def lb(self, ctx, page:int = 0):
        if await gamble_examine.if_file_exist(self, ctx):
            return

        name_info = self.gamble_info[ctx.guild.id][1]
        money_info = self.gamble_info[ctx.guild.id][3]
        currency_info = []

        currency_info = sorted(money_info, reverse = True)
        rank_msg = discord.Embed(title = "%sLeaderBoard"%":shrimp:", color = 0x11df60)
        count = 0
        last_currency = 0
        
        for sorted_currency in currency_info:
            count += 1
            if not page == 0:
                if count == 9:last_currency = sorted_currency
                if count > 9 * page : break
            elif page == 0:
                if count > 9 : break
            if not page == 0 and count <= 9 * (page - 1):  
                continue
            else:
                if count % 9 == 1: pass
                elif sorted_currency == last_currency:
                    del name_info[pos], money_info[pos]
                pos = money_info.index(sorted_currency)
                last_currency = sorted_currency
                rank_msg.add_field(name = "#%i "%count + name_info[pos], value = str(sorted_currency) + ":shrimp:", inline=True)
                
        await ctx.send(embed = rank_msg)
        await asyncio.sleep(0.75)
        await ctx.message.delete()

    @commands.command(
        help = "show your total money",
        brief = "show your total money"
    )
    async def info(self, ctx):
        if await gamble_examine.if_file_exist(self, ctx):
            return
        if await gamble_examine.is_valid(self, ctx, ctx.author.id):
            return
        
        pos = self.gamble_info[ctx.guild.id][2].index(ctx.author.id)
        name = "**" + ctx.author.name + "#" + ctx.author.discriminator + "**"
        text = "%s 擁有 %i%s" %(name, self.gamble_info[ctx.guild.id][3][pos], ":shrimp:")
        embed = discord.Embed(description = text, color = 0x11df60)
        await ctx.send(embed = embed)
        await asyncio.sleep(0.75)
        await ctx.message.delete()

    @commands.command(
        help = '''
        use this command by tagging the person you want to donate money to
        For example:
        ;donate @[name] 100
        ''',
        brief = "donate a certain amount to the person you want to donate"
    )
    async def donate(self, ctx, target:str = None, amount:int = 0):
        if await gamble_examine.if_file_exist(self, ctx):
            return
        if await gamble_examine.is_valid(self, ctx, ctx.author.id):
            return
        if await gamble_examine.is_amount_valid(self, ctx, ctx.author.id, amount):
            return

        if int(target[3:-1]) not in self.gamble_info[ctx.guild.id][2]:
            await ctx.send("target info doesn't exist")
            return
        else:
            donater_pos = self.gamble_info[ctx.guild.id][2].index(ctx.author.id)
            target_pos = self.gamble_info[ctx.guild.id][2].index(int(target[3:-1]))
            self.gamble_info[ctx.guild.id][3][donater_pos] -= amount
            self.gamble_info[ctx.guild.id][3][target_pos] += amount
            target_name = "**" + self.gamble_info[ctx.guild.id][1][target_pos] + "**"
            name = "**" + ctx.author.name + "#" + ctx.author.discriminator + "**"
            text = "%s 施捨了 %i%s給 %s" %(name, amount, ":shrimp:", target_name)
            embed = discord.Embed(description = text, color = 0x11df60)
            await ctx.send(embed = embed)
            await asyncio.sleep(0.75)
            await ctx.message.delete()

        with open(os.path.join("info", 'gamble_info'), 'wb') as f:
                pickle.dump(self.gamble_info, f)
            
def setup(bot):
    bot.add_cog(gamble_usage(bot, gamble_examine))
