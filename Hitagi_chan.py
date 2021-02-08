import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sys
from aiohttp import ClientSession
from datetime import datetime

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
MY_API_TOKEN = os.getenv('MY_API_TOKEN')
IMGUR_TOKEN = os.getenv('IMGUR_TOKEN')
bot = commands.Bot(command_prefix='/')
bot.remove_command('help')


@bot.event
async def on_ready():
    bot.aioSession = ClientSession()
    headers = {"Authorization": "Token "+MY_API_TOKEN}
    bot.aioSessionMy = ClientSession(headers=headers)
    headers = {"Authorization": "Client-ID "+IMGUR_TOKEN}
    bot.aioSessionIMGUR = ClientSession(headers=headers)
    print("Logged in as:",bot.user)
    try:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.{filename[:-3]}') 
    except Exception as err :
        print(f'Error loading Cog {filename[:-3]} err: {err}')
    
    print('Hitagi-chan is online')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="with Hanekawa-chan"))    

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    

@bot.event
async def on_guild_join(guild):
    channel = await bot.fetch_channel(762722885810651166)    
    await channel.send(f'```Hitagi-chan was added in {guild.name} {guild.id} guild```')
    for channel in guild.text_channels :
        if channel.permissions_for(guild.me).send_messages :
            await channel.send('Arigato!! for adding me \nPrefix is `/` \neg. `/help`')
            break

sys.path.append('.')
bot.run(DISCORD_BOT_TOKEN)
