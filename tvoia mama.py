import json
import random
import asyncio
import discord
import requests
import datetime
from PIL import Image
from bs4 import BeautifulSoup
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, SelectOption, Button, Select


d = 0
game_run = False
player = None


def get_mem_url(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    images = []

    link = requests.get('https://knowyourmeme.com/search?q='+query, headers=headers)
    html = BeautifulSoup(link.text, 'lxml')
    table = html.find('tbody', {'class':"entry-grid-body infinite"})
    pictures_code = table.find_all('a', {'class':"photo"})

    for i in pictures_code:
        images.append(i.find('img')["data-src"])
        
    random_picture = random.choice(images)
    return random_picture


def get_prefix(bot,message):

    with open('prefix.json',"r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix)

@bot.event
async def on_guild_join(guild):
    
    with open('prefix.json',"r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '>'

    with open('prefix.json',"w") as f:
        json.dump(prefixes,f)

@commands.has_permissions(administrator = True)
@bot.command()
async def changeprefix(ctx, prefix):

    with open('prefix.json',"r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefix.json',"w") as f:
        json.dump(prefixes,f)

    await ctx.send(f"The prefix was chenged to {prefix}")

@bot.event
async def on_message(msg):
    global game_run
    
    if not msg.content.isdigit():
        try:
            if msg.mentions[0] == client.user:
                with open('prefix.json',"r") as f:
                    prefixes = json.load(f)
                pre = prefixes[str(msg.guild.id)] = prefix
            await msg.channel.send(f"prefix - {pre}")
        except:
            pass
        await bot.process_commands(msg)
    elif game_run:
        messag = msg.content
        author = msg.author
        if author == player:
            number = int(messag)
            if d > number:
                await msg.channel.send('this number is bigger then ' + messag)
            elif d < number:
                await msg.channel.send('this number is smoller then ' + messag)
            else:
                game_run = False
                await msg.channel.send('OMGG!!!! 3KILL YOU ARE THE BEST MY NUMBER IS ' + messag + '!!!!!!!')

@bot.command()
async def mem(ctx, asd=None):
    if asd == None:
        await ctx.send('Genius plz enter the theme')
    else:
        await ctx.send(get_mem_url(asd))
    
@bot.command()
async def game(ctx, Max_number=None):
    if Max_number == None:
        await ctx.send("Specify number plz")
    else:
        await ctx.send("the diapozon 0 to " + Max_number)
        Max_numberr = int(Max_number)
        global player
        global d
        global game_run
        game_run = True
        player = ctx.message.author
        d = random.randint(0,Max_numberr)
    

bot.run('OTQ0NjYxNTA0OTIwMjc2OTky.YhE2lQ.mL2XnlxjJnOLgNX_BxDWjRZ0MRo')
