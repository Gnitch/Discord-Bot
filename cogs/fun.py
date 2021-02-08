import discord
from discord.ext import commands, tasks
import asyncio
import json
from aiohttp import ClientSession
from dotenv import load_dotenv
import os
from datetime import datetime, date
import calendar
import psycopg2
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):           
            await ctx.send('Type `/help` to check correct usage of commands')
            return  

    async def getSubredditFeed(self,url):
        try :          
            async with self.bot.aioSessionIMGUR.get(url) as response :
                if response.status != 200 :
                    return None                      
                res = await response.json()                    
                if len(res['data']) == 0 :
                    return None                   
            data = res['data']     
            len_ = len(data)
            ix = random.randint(0,len_-1)
            return data[ix]['link']

        except Exception as err :
            print(err)

    async def getAnimeQuote(self,query):
        query = query.strip()
        try :
            async with self.bot.aioSession.get('https://animechanapi.xyz/api/quotes'+query) as response :
                res = await response.json()  
                if response.status != 200 :
                    return None
                
                if len(res['data']) == 0 :
                    return None          
                
                return res['data']              

        except Exception as err :
            print(err)

    @commands.command(name='quote')
    async def animeQuotesByRandom(self,ctx): 
        data = await self.getAnimeQuote('/random')
        if data is not None :
            data = data[0]
            quote = data['quote']
            char = data['character']
            anime = data['anime']
            await ctx.send(f'```"{quote}"\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t-{char}({anime})```')
        else :
            await ctx.send(f'Error getting quote')

    @commands.command(name='an-meme')
    async def animeMayMay(self,ctx):
        now = datetime.now()
        hr = now.strftime('%H')
        if 0 <= int(hr) <= 12 :
            url = 'https://api.imgur.com/3/gallery/r/goodanimemes/time/1/day'
        elif 13 <= int(hr) <=17:
            url = 'https://api.imgur.com/3/gallery/r/goodanimemes/time/1/day'
        elif 18 <= int(hr) <= 20 :
            url = 'https://api.imgur.com/3/gallery/r/goodanimemes/time/1/day'
        elif 21 <= int(hr) <= 23 :
            url = 'https://api.imgur.com/3/gallery/r/goodanimemes/time/1/day'
        else :
            url = 'https://api.imgur.com/3/gallery/r/goodanimemes/time/1/day'      
                
        data = await self.getSubredditFeed(url)
        if data is not None :
            await ctx.send(data)
        else :
            await ctx.send('API ERROR\nTry again')

    @commands.command(name='wallpaper')
    async def animeWallpaper(self,ctx):
        now = datetime.now()
        hr = now.strftime('%H')
        if 0 <= int(hr) <= 12 :
            url = 'https://api.imgur.com/3/gallery/r/animewallpaper/time/1/day'
        elif 13 <= int(hr) <=17:
            url = 'https://api.imgur.com/3/gallery/r/animewallpaper/time/2/day'
        elif 18 <= int(hr) <= 20 :
            url = 'https://api.imgur.com/3/gallery/r/animewallpaper/time/3/day'
        elif 21 <= int(hr) <= 23 :
            url = 'https://api.imgur.com/3/gallery/r/animewallpaper/time/4/day'
        else :
            url = 'https://api.imgur.com/3/gallery/r/animewallpaper/time/1/day'                

        data = await self.getSubredditFeed(url)
        if data is not None :
            await ctx.send(data)
        else :
            await ctx.send('API ERROR\nTry again')  

    @commands.command(name='waifu')
    async def getWaifu(self,ctx,*,query):
        if query.startswith('<@!') and query.endswith('>'):
            ix = int(query[-3:-1])
            if ix > 25 :
                ix = int(query[-2])
            f = open(r'utils\WaifuList.json')
            data = json.load(f)
            if data is not None :
                i = 0
                for item in data.items() :
                    i += 1
                    if i == ix :
                        name = item[0]
                        info = item[1]['url']
                        break
                            
                await ctx.send(f'**{name}** \n{info}')

            else :
                await ctx.send('No Waifu found')
        else :
            await ctx.send('Tag a member')

def setup(bot):
    bot.add_cog(Fun(bot))