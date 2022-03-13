import discord
import random
import datetime
import pickle
import os
import asyncio
from gamble_config import gamble_examine
from discord.ext import commands, tasks

# generate random seed for module random
seed = "".join(random.sample("0123456789abcdefghijklmnopqrstuvwxyz",random.randint(6, 15)))
random.seed(seed)

class gamble_entertainment(commands.Cog):
    def __init__(self, bot, gamble_examine):
        self.gamble_examine = gamble_examine
        
        self.bot = bot
        self.gamble_info = {}
    
    @commands.command(
        help = '''
        use this command to bet your money
        For example:
        ;wheel 50
        ''',
        brief = "use this command to bet your money"
    )
    async def wheel(self, ctx, amount:int = 0):
        if await gamble_examine.if_file_exist(self, ctx):
            return
        if await gamble_examine.is_valid(self, ctx, ctx.author.id):
            return
        if await gamble_examine.is_amount_valid(self, ctx, ctx.author.id, amount):
            return

        # variable for later use
        pos = self.gamble_info[ctx.guild.id][2].index(ctx.author.id)
        self.gamble_info[ctx.guild.id][3][pos] -= amount
        name = ctx.author.name + "#" + ctx.author.discriminator

        # choose random direction for wheel and update player info
        way = {":arrow_upper_left:":1.4, ":arrow_up:":1.9, ":arrow_upper_right:":2.5, ":arrow_left:":0.2, ":arrow_right:":1.2, ":arrow_lower_left:":0.1, ":arrow_down:":0.3, ":arrow_lower_right:":0.5}
        direction = random.choice(list(way.keys()))
        self.gamble_info[ctx.guild.id][3][pos] += int(round(amount*way[direction]))

        # build result message and send, delete the command message
        text = "\n『1.4』  『1.9』  『2.5』\n\n『0.2』      %s       『1.2』\n\n『0.1』  『0.3』  『0.5』\n" %direction
        embed = discord.Embed(title = text, color = 0x11df60)
        embed.set_author(name = "%s  won : %i🦐" %(name, int(round(amount*way[direction]))))
        await ctx.send(embed = embed)
        await asyncio.sleep(0.75)
        await ctx.message.delete()

        with open(os.path.join( "info", 'gamble_info'), 'wb') as f:
            pickle.dump(self.gamble_info, f)

    @commands.command(
        help = '''
        flip a coin and guess which direction it is facing
        for example:
        ;bf 50 h
        ''',
        brief = "flip a coin and guess"
    )
    async def bf(self, ctx, amount:int = 0, headortail:str = None):
        if await gamble_examine.if_file_exist(self, ctx):
            return
        if await gamble_examine.is_valid(self, ctx, ctx.author.id):
            return
        if await gamble_examine.is_amount_valid(self, ctx, ctx.author.id, amount):
            return

        # check if the orientation is valid
        if headortail == None:
            await ctx.send("請輸入正面或反面")
            return
        elif (not headortail == "h") and (not headortail == "t"):
            await ctx.send("error")
            return

        # variables for later use and choose random coin orientation
        pos = self.gamble_info[ctx.guild.id][2].index(ctx.author.id)
        coin = {"h":"https://nadeko-pictures.nyc3.digitaloceanspaces.com/coins/heads3.png",
                "t":"https://nadeko-pictures.nyc3.digitaloceanspaces.com/coins/tails3.png"}
        self.gamble_info[ctx.guild.id][3][pos] -= amount
        name = "**" + ctx.author.name + "#" + ctx.author.discriminator + "**"
        ht = random.choice(list(coin.keys()))

        # generate and send result message
        if headortail == ht:
            self.gamble_info[ctx.guild.id][3][pos] += int(round(amount*2.2))
            text = "%s 您猜對了! 您贏得了 %i%s" %(name, int(round(amount*2.2)), ":shrimp:")
        else:
            text = "%s 再接再厲, 下次會更好(￣y▽,￣)╭ " %name
        embed = discord.Embed(description = text, color = 0x11df60)
        embed.set_image(url = coin[ht])
        await ctx.send(embed = embed)
        await asyncio.sleep(0.75)
        await ctx.message.delete()

        with open(os.path.join( "info", 'gamble_info'), 'wb') as f:
            pickle.dump(self.gamble_info, f)

    @commands.command(
        help = '''
        Bets a certain amount of money by rolling a dice, rolling over 66 yields x2 of your currency, over 90 -> x4 and over 100 -> x10
        for example:
        ;br 100
        ''',
        brief = "Bets a certain amount of money by rolling a dice"
    )
    async def br(self, ctx, amount:int = 0):
        if await gamble_examine.if_file_exist(self, ctx):
            return
        if await gamble_examine.is_valid(self, ctx, ctx.author.id):
            return
        if await gamble_examine.is_amount_valid(self, ctx, ctx.author.id, amount):
            return

        # variables for later use and random dice points
        pos = self.gamble_info[ctx.guild.id][2].index(ctx.author.id)
        self.gamble_info[ctx.guild.id][3][pos] -= amount
        dice = random.randint(1,100)
        name = "**" + ctx.author.name + "#" + ctx.author.discriminator + "**"

        # judge result
        if dice == 1:
            amount = amount * 5
            reason = "骰出 1 點"
        elif dice > 65 and dice < 90:
            amount = amount * 2
            reason = "骰出高於 66 點"
        elif dice > 89 and dice < 100:
            amount = amount * 4
            reason = "骰出高於 90 點"
        elif dice == 100:
            amount = amount * 10
            reason = "骰出 100 點"
        else:
            amount = 0
            reason = "點數低於 66 "

        # send result message and update player data
        text = "%s 您骰出了 %i, 恭喜!您因%s而獲得了 %i%s" %(name, dice, reason, amount, ":shrimp:")
        self.gamble_info[ctx.guild.id][3][pos] += amount
        embed = discord.Embed(description = text, color = 0x11df60)
        await ctx.send(embed = embed)
        await asyncio.sleep(0.75)
        await ctx.message.delete()
        
        with open(os.path.join( "info", 'gamble_info'), 'wb') as f:
            pickle.dump(self.gamble_info, f)

    @commands.command(
        help = "withdraw your money every 9 hours",
        brief = "withdraw your money"
    )
    async def timely(self, ctx):
        # judge if file exist and create a new one if no
        if os.path.isfile("info/gamble_info"):
            pass
        else:
            with open(os.path.join( "info", 'gamble_info'), 'wb') as f:
                pickle.dump(self.gamble_info, f)
        
        with open(os.path.join( "info", 'gamble_info'), 'rb') as f:
            self.gamble_info = pickle.load(f)

        # variables for later use
        claimtime = datetime.datetime.now() + datetime.timedelta(hours = 9)
        name = "**" + ctx.author.name + "#" + ctx.author.discriminator + "**"

        # check if member info is in the file
        if ctx.guild.id not in self.gamble_info:
            self.gamble_info[ctx.guild.id] = []
            self.gamble_info[ctx.guild.id].append(ctx.guild.name)
            for i in range(4): self.gamble_info[ctx.guild.id].append([])
        else:
            pass

        # check time and cooldown
        if ctx.author.id not in self.gamble_info[ctx.guild.id][2]:
            self.gamble_info[ctx.guild.id][1].append(name[2:-2])
            self.gamble_info[ctx.guild.id][2].append(ctx.author.id)
            self.gamble_info[ctx.guild.id][3].append(1000)
            self.gamble_info[ctx.guild.id][4].append(claimtime) 
            text = "%s 已領取1000%s, 9小時候可以再領一次" %(name, ":shrimp:")
            color = 0x11df60
        else:
            pos = self.gamble_info[ctx.guild.id][2].index(ctx.author.id)      
            if datetime.datetime.now() > self.gamble_info[ctx.guild.id][4][pos]:
                self.gamble_info[ctx.guild.id][3][pos] += 1000
                self.gamble_info[ctx.guild.id][4][pos] = claimtime
                text = "%s 已領取1000%s, 9小時候可以再領一次" %(name, ":shrimp:")
                color = 0x11df60
            else:
                time = self.gamble_info[ctx.guild.id][4][pos] - datetime.datetime.now()
                h, m, s = str(time).split(":")
                lasttime = "%s小時%s分%s秒" %(h, m, s[:-7])
                text = "%s 您已經領取獎勵, 距離下次領取還有%s" %(name, lasttime)
                color = 0xdf3434

        # send result message update file
        embed = discord.Embed(description = text, color = color)
        await ctx.send(embed = embed)
        await asyncio.sleep(0.75)
        await ctx.message.delete()
        
        with open(os.path.join( "info", 'gamble_info'), 'wb') as f:
            pickle.dump(self.gamble_info, f)
            
def setup(bot):
    bot.add_cog(gamble_entertainment(bot, gamble_examine))
