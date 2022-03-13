import json
import random
import discord
import os
from discord.ext import commands

with open(os.path.join("..", "info", 'setting.json'),'r',encoding='utf8')as jfile:
    jdata = json.load(jfile) 

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '[', intents=intents)

seed = "".join(random.sample("0123456789abcdefghijklmnopqrstuvwxyz",random.randint(6, 15)))

with open(os.path.join("..", "info", "extension.txt"), 'r') as f:
    for extension in f:
        bot.load_extension(extension.strip('\n'))

@bot.event
async def on_ready():
    print('bot is online')
    game = discord.Game("遊戲")
    await bot.change_presence(activity = game)

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

bot.run(jdata['TOKEN'])
