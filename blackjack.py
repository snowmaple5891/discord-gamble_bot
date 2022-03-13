import discord
import asyncio
import datetime
import pickle
import os
from random import randint
from gamble_config import gamble_examine
from discord.ext import commands

class bj(commands.Cog):
    def __init__(self, bot, gamble_examine):
        self.gamble_examine = gamble_examine
        
        self.bot = bot
        self.bj_detail = []
        self.deck_detail = {}
        self.gamble_info = {}

    # pull cards for dealer
    async def dealer_pull(self):
        random_card_generator = (randint(0, self.deck_detail["total_cards"] - 1))
        self.bj_detail[0]["dealer"]["dealer_deck"].append(self.deck_detail["card_deck"][random_card_generator])
        self.deck_detail["card_deck"].pop(random_card_generator)
        self.deck_detail["total_cards"] -= 1
        self.bj_detail[0]["dealer"]["dealer_point"] = await self.cal_tpoint(self.bj_detail[0]["dealer"]["dealer_deck"], True)

    # calculate total points
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
                if max(totalp) > 16 and max(totalp) < 22: return max(totalp)
                elif max(totalp) < 17: return min(totalp)
                elif max(totalp) > 21: return min(totalp)
            return totalp
        return total

    # pull random cards and update players info
    async def selectcard(self, player):
        random_card_generator = (randint(0, self.deck_detail["total_cards"] - 1))
        if self.deck_detail["card_deck"][random_card_generator][:-2] == "1":
            self.bj_detail[0]["member_info"][player]["hasA"] = True
        self.bj_detail[0]["member_info"][player]["hand"].append(self.deck_detail["card_deck"][random_card_generator])
        self.deck_detail["card_deck"].pop(random_card_generator)
        self.deck_detail["total_cards"] -= 1

    # generate DM message and string for total points
    async def generate_dmmsg(self, player, cards:str):
        tpoints = await self.cal_tpoint(self.bj_detail[0]["member_info"][player]["hand"])
        if self.bj_detail[0]["member_info"][player]["hasA"]:
            tpmsg = str(tpoints[0]) + " or " + str(tpoints[1])
        else: tpmsg = tpoints
        DMmsg = discord.Embed(title = "Your cards are %s"%cards[:-2], description = "total points: %s"%str(tpmsg))
        return DMmsg, tpoints

    @commands.command(hidden = True)
    async def stand(self, ctx):
        self.bot.appinfo = await self.bot.application_info()
        channel = await self.bot.fetch_channel(self.bj_detail[0]["channel_id"])
        msg = await channel.fetch_message(self.bj_detail[0]["bj_msgid"])
        guild_id = channel.guild.id
        
        # update player info and status
        self.bj_detail[0]["member_info"][ctx.author]["total"] = await self.cal_tpoint(self.bj_detail[0]["member_info"][ctx.author]["hand"])
        self.bj_detail[0]["member_info"][ctx.author]["ifstop"] = True
        
        # create and send hyperlink for players to transfer to the channel where they start the game 
        bjresult = self.bj_detail[0]["bj_text"]
        jump = discord.Embed(title = "click here to transfer to BlackJack table", description = "please wait for orther players to finish their operation",  url = msg.jump_url)
        await ctx.send(embed = jump)

        # judge if all players have stopped
        for member in self.bj_detail[0]["member_info"]:
            if not self.bj_detail[0]["member_info"][member]["ifstop"]:
                return
        
        # pull dealers card and update embed blackjack message
        await self.dealer_pull()
        while self.bj_detail[0]["dealer"]["dealer_point"] < 17:
            await self.dealer_pull()
        dealer_card = ""
        d_point = self.bj_detail[0]["dealer"]["dealer_point"]
        for i in range(len(self.bj_detail[0]["dealer"]["dealer_deck"])):
            dealer_card += self.bj_detail[0]["dealer"]["dealer_deck"][i] + ", "
        bjresult.remove_field(0)
        bjresult.insert_field_at(0, name = "**%s**"%self.bot.appinfo.name, value = "Dealer's card: %s\ntotal points: %s"%(dealer_card[:-2], d_point), inline = False)
        
        # judge all players result
        for r_member in self.bj_detail[0]["member_info"]:
            if_win = "lose"
            total = self.bj_detail[0]["member_info"][r_member]["total"]
            if self.bj_detail[0]["member_info"][r_member]["hasA"] and max(total) <= 21:
                total = max(total)
            elif self.bj_detail[0]["member_info"][r_member]["hasA"]:
                total = min(total)
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

            # update member currency in the guild
            if if_win == "win":
                pos = self.gamble_info[guild_id][2].index(r_member.id)
                self.gamble_info[guild_id][3][pos] += (int(self.bj_detail[0]["member_info"][r_member]["amount"])) * 2

                with open(os.path.join( "info", 'gamble_info'), 'wb') as f:
                    pickle.dump(self.gamble_info, f)
              
            # edit embed blackjack message
            f_index = self.bj_detail[0]["member_info"][r_member]["field_index"]
            cards_text = ""
            for l in range(len(self.bj_detail[0]["member_info"][r_member]["hand"])):
                cards_text += self.bj_detail[0]["member_info"][r_member]["hand"][l] + ", "
            bjresult.remove_field(f_index)
            bjresult.insert_field_at(f_index, name = "**%s**-%s"%(r_member.name, if_win), value = "your card: %s\ntotal points: %s"%(cards_text[:-2], total), inline = False)
        
        # get time when the game ended
        now = datetime.datetime.today() + datetime.timedelta(hours = 8)
        datetime_str = now.strftime("%Y/%m/%d %H:%M:%S")
        bjresult.set_footer(text = "已於 " + datetime_str + " - 結束")
        await msg.edit(embed = bjresult)

        # clear all data
        self.bj_detail = []
        self.deck_detail = {}

    @commands.command(hidden = True)
    async def hit(self, ctx):
        if not self.bj_detail[0]["member_info"][ctx.author]["ifstop"]:
            cards = ""
            # pull a card and generate card info message
            await self.selectcard(ctx.author)
            for i in range(len(self.bj_detail[0]["member_info"][ctx.author]["hand"])):
                cards += self.bj_detail[0]["member_info"][ctx.author]["hand"][i] + ", "
            hasA = self.bj_detail[0]["member_info"][ctx.author]["hasA"]
            DMmsg_update, tpoints = await self.generate_dmmsg(ctx.author, cards)
            dmmsg = await ctx.author.fetch_message(self.bj_detail[0]["member_info"][ctx.author]["dmmsg_id"])
            if hasA:totalpoint = min(tpoints)
            else: totalpoint = tpoints

            # judge if total points players own is valid
            if len(self.bj_detail[0]["member_info"][ctx.author]["hand"]) == 5 and totalpoint < 21:
                self.bj_detail[0]["member_info"][ctx.author]["pass5"] = True
                self.bj_detail[0]["member_info"][ctx.author]["ifstop"] = True
            elif totalpoint > 21:
                self.bj_detail[0]["member_info"][ctx.author]["ifstop"] = True
            self.bj_detail[0]["member_info"][ctx.author]["total"] = totalpoint
            
            # update players card detail and message
            await dmmsg.edit(embed = DMmsg_update)
            if len(self.bj_detail[0]["member_info"]) == 1: await ctx.send("please use the command ;stand to end the game")
        else:
            await ctx.send("you can't call anymore") 

    @commands.command(hidden = True)
    async def startgame(self, ctx):
        if self.bj_detail[0]["if_start"]:
            await ctx.send("game has already started, it can't be started again")
            await asyncio.sleep(0.75)
            await ctx.message.delete()
            return

        self.bj_detail[0]["if_start"] = True
        
        # pull dealer's card and update embed blackjack message
        self.bot.appinfo = await self.bot.application_info()
        await self.dealer_pull()
        bj_text_update = self.bj_detail[0]["bj_text"]
        bj_text_update.remove_field(0)
        dealer_card = self.bj_detail[0]["dealer"]["dealer_deck"][0]
        bj_text_update.insert_field_at(0, name = "**%s**"%self.bot.appinfo.name, value = "Dealer's card: %s, ?\ntotal points: ?"%dealer_card, inline = False)
        
        bj_msg = await ctx.channel.fetch_message(self.bj_detail[0]["bj_msgid"])
        await bj_msg.edit(embed = bj_text_update)

        # send DM message to all players
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

    @commands.command(hidden = True)
    async def joingame(self, ctx, amount:int = 0):
        if self.bj_detail[0]["if_start"]:
            await ctx.send("game has already started, please wait for next game")
            await asyncio.sleep(0.75)
            await ctx.message.delete()
            return

        if await gamble_examine.if_file_exist(self, ctx):
            return
        if await gamble_examine.is_valid(self, ctx, ctx.author.id):
            return
        if await gamble_examine.is_amount_valid(self, ctx, ctx.author.id, amount):
            return

        pos = self.gamble_info[ctx.guild.id][2].index(ctx.author.id)
        self.gamble_info[ctx.guild.id][3][pos] -= amount

        with open(os.path.join( "info", 'gamble_info'), 'wb') as f:
            pickle.dump(self.gamble_info, f)
            
        # create and save player info
        self.bj_detail[0]["member_info"][ctx.author] = {"amount":amount, "hand":[], "total":0, "field_index":len(self.bj_detail[0]["member_info"]) + 1, "hasA":False, "dmmsg_id":0, "pass5":False, "ifstop":False}

        #update embed blackjack message
        bj_text_update = self.bj_detail[0]["bj_text"]
        bj_text_update.add_field(name = "**" + ctx.author.name + "**", value = "your card: \ntotal points:", inline = False)

        bj_msg = await ctx.channel.fetch_message(self.bj_detail[0]["bj_msgid"])
        await bj_msg.edit(embed = bj_text_update)

        self.bj_detail[0]["bj_text"] = bj_text_update
        await ctx.message.delete()

    @commands.command(hidden = True)
    async def create_bjgame(self, ctx):
        # create blackjack game text
        self.bot.appinfo = await self.bot.application_info()
        bj_table_text = discord.Embed(description = "K, Q, J = 10 | A = 1 or 11")
        bj_table_text.set_author(name="%sの BlackJack Game"%self.bot.appinfo.name, icon_url=self.bot.appinfo.icon_url)
        bj_table_text.add_field(name = "**%s**"%self.bot.appinfo.name, value = "Dealer's card: \ntotal points: ", inline = False)

        # see if another blackjack game is in process in the same time
        if len(self.bj_detail) > 0:
            await ctx.send("another BlackJack game is in process, plese wait until the game is over")
            await ctx.message.delete()
            return

        # create card deck list and save total amounts of  cards 
        self.deck_detail["total_cards"] = 312
        self.deck_detail["card_deck"] = []
        self.deck_detail["not int"] = ['J', 'Q', 'K']

        # create 6 decks of cards and append it into card deck
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

        # create file to save all players info and blackjack text message
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

    @commands.command(hidden = True)
    async def showbj(self, ctx):
        await ctx.send(self.bj_detail)

def setup(bot):
    bot.add_cog(bj(bot, gamble_examine))
