import discord
import asyncio
import datetime
from random import randint
from discord.ext import commands

class bj(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bj_detail = []
        self.deck_detail = {}

    async def dealer_pull(self):
        random_card_generator = (randint(0, self.deck_detail["total_cards"] - 1))
        self.bj_detail[0]["dealer"]["dealer_deck"].append(self.deck_detail["card_deck"][random_card_generator])
        self.deck_detail["card_deck"].pop(random_card_generator)
        self.deck_detail["total_cards"] -= 1
        self.bj_detail[0]["dealer"]["dealer_point"] = await self.cal_tpoint(self.bj_detail[0]["dealer"]["dealer_deck"], True)

    async def cal_tpoint(self, hand:list, dealer = False):
        total = 0
        Acount = 0
        hasA = False
        for i in hand: 
            if i[:-2] in self.deck_detail["not int"]:
                total += 10
            else:
                if i[:-2] == "1":
                    Acount += 1
                    hasA = True
                    continue
                total += int(i[:-2])
        if hasA:
            totalp = []
            totalp.append(total + Acount)
            totalp.append(total + Acount + 10)
            if dealer: 
                if max(totalp) > 21: return min(totalp)
                return max(totalp)
            return totalp
        return total

    async def selectcard(self, player):
        random_card_generator = (randint(0, self.deck_detail["total_cards"] - 1))
        if self.deck_detail["card_deck"][random_card_generator][:-2] == "1":
            self.bj_detail[0]["member_info"][player]["hasA"] = True
        self.bj_detail[0]["member_info"][player]["hand"].append(self.deck_detail["card_deck"][random_card_generator])
        self.deck_detail["card_deck"].pop(random_card_generator)
        self.deck_detail["total_cards"] -= 1

    async def generate_dmmsg(self, player, cards:str):
        tpoints = await self.cal_tpoint(self.bj_detail[0]["member_info"][player]["hand"])
        if self.bj_detail[0]["member_info"][player]["hasA"]:
            tpmsg = str(tpoints[0]) + " or " + str(tpoints[1])
        else: tpmsg = tpoints
        DMmsg = discord.Embed(title = "Your cards are %s"%cards[:-2], description = "total points: %s"%str(tpmsg))
        return DMmsg, tpoints

    @commands.command()
    async def stop(self, ctx):
        self.bj_detail[0]["member_info"][ctx.author]["total"] = await self.cal_tpoint(self.bj_detail[0]["member_info"][ctx.author]["hand"])
        self.bj_detail[0]["member_info"][ctx.author]["ifstop"] = True
        channel = await self.bot.fetch_channel(self.bj_detail[0]["channel_id"])
        msg = await channel.fetch_message(self.bj_detail[0]["bj_msgid"])
        bjresult = self.bj_detail[0]["bj_text"]
        jump = discord.Embed(title = "click here to transfer to BlackJack table", description = "please wait for orther players to finish their operation",  url = msg.jump_url)
        await ctx.send(embed = jump)
        for member in self.bj_detail[0]["member_info"]:
            if not self.bj_detail[0]["member_info"][member]["ifstop"]:
                return
        await self.dealer_pull()
        while self.bj_detail[0]["dealer"]["dealer_point"] < 17:
            await self.dealer_pull()
        bjresult.remove_field(0)
        dealer_card = ""
        d_point = self.bj_detail[0]["dealer"]["dealer_point"]
        for i in range(len(self.bj_detail[0]["dealer"]["dealer_deck"])):
            dealer_card += self.bj_detail[0]["dealer"]["dealer_deck"][i] + ", "
        bjresult.insert_field_at(0, name = "**賭博BOT**", value = "Dealer's card: %s\ntotal points: %s"%(dealer_card[:-2], d_point), inline = False)
        for r_member in self.bj_detail[0]["member_info"]:
            if_win = "lose"
            total = self.bj_detail[0]["member_info"][r_member]["total"]
            print(total)
            if self.bj_detail[0]["member_info"][r_member]["pass5"]:
                if_win = "win"
            elif total > 21:
                pass
            elif self.bj_detail[0]["dealer"]["dealer_point"] > 21:
                if_win = "win"
            elif total > self.bj_detail[0]["dealer"]["dealer_point"]:
                if_win = "win"
            elif total == self.bj_detail[0]["dealer"]["dealer_point"]:
                if_win = "lose"
            else:
                pass
            f_index = self.bj_detail[0]["member_info"][r_member]["field_index"]
            cards_text = ""
            for l in range(len(self.bj_detail[0]["member_info"][r_member]["hand"])):
                cards_text += self.bj_detail[0]["member_info"][r_member]["hand"][l] + ", "
            bjresult.remove_field(f_index)
            bjresult.insert_field_at(f_index, name = "**%s**-%s"%(r_member.name, if_win), value = "your card: %s\ntotal points: %s"%(cards_text[:-2], total), inline = False)
        now = datetime.datetime.today()
        datetime_str = now.strftime("%Y/%m/%d %H:%M:%S")
        bjresult.set_footer(text = "已於 " + datetime_str + " - 結束")
        await msg.edit(embed = bjresult)
        self.bj_detail = []
        self.deck_detail = {}

    @commands.command()
    async def call(self, ctx):
        if not self.bj_detail[0]["member_info"][ctx.author]["ifstop"]:
            cards = ""
            await self.selectcard(ctx.author)
            for i in range(len(self.bj_detail[0]["member_info"][ctx.author]["hand"])):
                cards += self.bj_detail[0]["member_info"][ctx.author]["hand"][i] + ", "
            hasA = self.bj_detail[0]["member_info"][ctx.author]["hasA"]
            DMmsg_update, tpoints = await self.generate_dmmsg(ctx.author, cards)
            dmmsg = await ctx.author.fetch_message(self.bj_detail[0]["member_info"][ctx.author]["dmmsg_id"])
            if hasA:totalpoint = min(tpoints)
            else: totalpoint = tpoints
            if len(self.bj_detail[0]["member_info"][ctx.author]["hand"]) == 5 and totalpoint < 21:
                self.bj_detail[0]["member_info"][ctx.author]["pass5"] = True
                self.bj_detail[0]["member_info"][ctx.author]["ifstop"] = True
            elif totalpoint > 21:
                self.bj_detail[0]["member_info"][ctx.author]["ifstop"] = True
            self.bj_detail[0]["member_info"][ctx.author]["total"] = totalpoint
            await dmmsg.edit(embed = DMmsg_update)
            if len(self.bj_detail[0]["member_info"]) == 1: await ctx.send("please use the command [stop to end the game")
        else:
            await ctx.send("you can't call anymore") 

    @commands.command()
    async def startgame(self, ctx):
        if self.bj_detail[0]["if_start"]:
            await ctx.send("game has already started, it can't be started again")
            await asyncio.sleep(0.75)
            await ctx.message.delete()
            return
        
        await self.dealer_pull()
        bj_text_update = self.bj_detail[0]["bj_text"]
        bj_text_update.remove_field(0)
        dealer_card = self.bj_detail[0]["dealer"]["dealer_deck"][0]
        bj_text_update.insert_field_at(0, name = "**賭博BOT**", value = "Dealer's card: %s, ?\ntotal points: ?"%dealer_card, inline = False)
        
        bj_msg = await ctx.channel.fetch_message(self.bj_detail[0]["bj_msgid"])
        await bj_msg.edit(embed = bj_text_update)

        self.bj_detail[0]["bj_text"] = bj_text_update
        for member in self.bj_detail[0]["member_info"]:
            cards = ""
            for i in range(2):
                await self.selectcard(member)
                cards += self.bj_detail[0]["member_info"][member]["hand"][i] + ", "
            DMmsg, tpoints = await self.generate_dmmsg(member, cards)
            dmmsg = await member.send(embed = DMmsg)
            self.bj_detail[0]["member_info"][member]["dmmsg_id"] = dmmsg.id
        await ctx.message.delete()

    @commands.command()
    async def joingame(self, ctx, amount):
        if self.bj_detail[0]["if_start"]:
            await ctx.send("game has already started, please wait for next game")
            await asyncio.sleep(0.75)
            await ctx.message.delete()
            return

        self.bj_detail[0]["member_info"][ctx.author] = {"amount":amount, "hand":[], "total":0, "field_index":len(self.bj_detail[0]["member_info"]) + 1, "hasA":False, "dmmsg_id":0, "pass5":False, "ifstop":False}

        bj_text_update = self.bj_detail[0]["bj_text"]
        bj_text_update.add_field(name = "**" + ctx.author.name + "**", value = "your card: \ntotal points:", inline = False)

        bj_msg = await ctx.channel.fetch_message(self.bj_detail[0]["bj_msgid"])
        await bj_msg.edit(embed = bj_text_update)

        self.bj_detail[0]["bj_text"] = bj_text_update
        await ctx.message.delete()

    @commands.command()
    async def creat_bjgame(self, ctx):
        bj_table_text = discord.Embed(description = "K, Q, J = 10 | A = 1 or 11")
        bj_table_text.set_author(name="賭博BOT の BlackJack Game", icon_url="https://cdn.discordapp.com/attachments/861854219991908352/949686616476233768/unknown.png")
        bj_table_text.add_field(name = "**賭博BOT**", value = "Dealer's card: \ntotal points: ", inline = False)

        if len(self.bj_detail) > 0:
            await ctx.send("another BlackJack game is in process, plese wait until the game is over")
            await asyncio.sleep(0.75)
            await ctx.message.delete()
            return

        self.deck_detail["total_cards"] = 312
        self.deck_detail["card_deck"] = []
        self.deck_detail["not int"] = ['J', 'Q', 'K']

        for i in range(1,11):
            for j in range(1,5):
                words = ""
                if j == 1:
                    words = "%d-%s" %(i ,"♧")
                    for z in range(6): self.deck_detail["card_deck"].append(words)
                if j == 2:
                    words = "%d-%s" %(i ,"♢")
                    for z in range(6): self.deck_detail["card_deck"].append(words)
                if j == 3:
                    words = "%d-%s" %(i ,"♡")
                    for z in range(6): self.deck_detail["card_deck"].append(words)
                if j == 4:
                    words = "%d-%s" %(i ,"♤")
                    for z in range(6): self.deck_detail["card_deck"].append(words)

        for j in range(1,5):
            for i in range(3):
                if j == 1:
                    words1 = "%s-%s" %(self.deck_detail["not int"][i] ,"♧")
                    for z in range(6): self.deck_detail["card_deck"].append(words1)
                elif j == 2:
                    words1 = "%s-%s" %(self.deck_detail["not int"][i] ,"♢")
                    for z in range(6): self.deck_detail["card_deck"].append(words1)
                elif j == 3:
                    words1 = "%s-%s" %(self.deck_detail["not int"][i] ,"♡")
                    for z in range(6): self.deck_detail["card_deck"].append(words1)
                elif j == 4:
                    words1 = "%s-%s" %(self.deck_detail["not int"][i] ,"♤")
                    for z in range(6): self.deck_detail["card_deck"].append(words1)

        temp = {}
        temp["channel_id"] = ctx.channel.id
        temp["if_start"] = False
        temp["member_info"] = {}
        temp["dealer"] = {"dealer_deck":[], "dealer_point":0}
        table_msg = await ctx.send(embed = bj_table_text)
        temp["bj_text"] = bj_table_text
        temp["bj_msgid"] = table_msg.id
        self.bj_detail.append(temp)
     
        await asyncio.sleep(0.75)
        await ctx.message.delete()

    @commands.command()
    async def showbj(self, ctx):
        await ctx.send(self.bj_detail)

def setup(bot):
    bot.add_cog(bj(bot))