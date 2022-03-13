import json
import random
import asyncio
import time
from datetime import datetime, time, timedelta
import discord
import os
from discord.ext import tasks, commands

with open(os.path.join("..", "info", 'setting.json'),'r',encoding='utf8')as jfile:
    jdata = json.load(jfile) 

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '[', intents=intents)

seed = "".join(random.sample("0123456789abcdefghijklmnopqrstuvwxyz",random.randint(6, 15)))

with open(os.path.join("..", "info", "extension.txt"), 'r') as f:
    for extension in f:
        bot.load_extension(extension.strip('\n'))
        
count = 0

@tasks.loop(seconds=60)
async def printer():
    global count
    channel = bot.get_channel(947526426414956616)
    await channel.send('%i'%count)
    count += 1
    
@printer.before_loop
async def before_printer():
    print('waiting...')
    await bot.wait_until_ready()

printer.start()

@bot.event
async def on_ready():
    print('bot is online')
    game = discord.Game("遊戲")
    await bot.change_presence(activity = game)

@bot.event
async def on_message(msg):
    if msg.content == "G":
        await msg.channel.send("GG")
    await bot.process_commands(msg)

@bot.command(help = "Load extension.", brief = "Load extension.")
async def load(ctx, extension): # extension: 使用者輸入要加入的功能
    try:
        bot.load_extension(extension.lower()) # load extension, lower() 因為檔名是小寫
        await ctx.send(f"{extension} loaded.") # Bot 傳送訊息
    except Exception as e:
        await ctx.send(e) # 若加入失敗印出錯誤訊息

# unload extension 卸載功能
@bot.command(help = "Un-load extension.", brief = "Un-load extension.")
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension.lower()) # load extension, lower() 因為檔名是小寫
        await ctx.send(f"{extension} unloaded.") # Bot 傳送訊息
    except Exception as e:
        await ctx.send(e) # 若加入失敗印出錯誤訊息

# reload extension 重新加入功能
@bot.command(help = "Re-load extension.", brief = "Re-load extension.")
async def reload(ctx, extension):
    try:
        bot.reload_extension(extension.lower()) # load extension, lower() 因為檔名是小寫
        await ctx.send(f"{extension} reloaded.") # Bot 傳送訊息
    except Exception as e:
        await ctx.send(e) # 若加入失敗印出錯誤訊息

# bot.loop.create_task(background_task())
bot.run(jdata['TOKEN'])

# @bot.command()
# async def rules(ctx):
#     timely = discord.Embed(color=0xf66213)
#     timely.add_field(name = "~timely", value = "Use this command to get your \"timely\" currency, you can withdraw your money every 3 hours", inline=False)
#     timely.add_field(name = "使用方式:", value = "~timely", inline=False)
#     betroll = discord.Embed(color=0xf66213)
#     betroll.add_field(name = "~betroll", value = "Bets a certain amount of money by rolling a dice, rolling over 66 yields x2 of your currency, over 90 -> x4 and over 100 -> x10", inline = False)
#     betroll.add_field(name = "使用方式:", value = "~betroll 20", inline = False)
#     wheel = discord.Embed(color=0xf66213)
#     wheel.add_field(name = "~wheel", value = "Bets a certain amount of money by spinning the ring of fortune, the result is how much to multiple your currency, whether win or lose is decided by your own luck", inline=False)
#     wheel.add_field(name = "使用方式:", value = "~wheel 200", inline=False)
#     info = discord.Embed(color=0xf66213)
#     info.add_field(name = "~info", value = "show your account detail like total money and your rank among all the people playing this", inline=False)
#     info.add_field(name = "使用方式:", value = "~info", inline=False)
#     donate = discord.Embed(color=0xf66213)
#     donate.add_field(name = "~donate", value = "donate money to someone else, tag the person you want to donate to, you can't donate if you don't have enough money", inline=False)
#     donate.add_field(name = "使用方式:", value = "~donate @RAINEKOwO 100", inline=False)
#     await ctx.send(embed = timely)
#     await ctx.send(embed = betroll)
#     await ctx.send(embed = wheel)
#     await ctx.send(embed = donate)
#     await ctx.send(embed = info)