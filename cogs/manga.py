import discord
from discord.ext import commands, tasks
import asyncio
import json
from aiohttp import ClientSession
from dotenv import load_dotenv
import os
from datetime import datetime, date
import calendar

from utils import AnimeMangaUtil

class Manga(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        # self.postAnimeSchedule.start() #Enable During production
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):           
            await ctx.send('Type `/help` to check correct usage of commands')
            return           

    @commands.command(name='manga',aliases=['mn'])
    async def mangaSearch(self,ctx, *,query):
        page = 0
        ix = 0  
        data = await AnimeMangaUtil.searchAnimeMangaDesc(self.bot,query,'manga')     
        if data is None or query is None:
            await ctx.send(f'No Manga found')
        elif data == 0:
            await ctx.send(f'API Error \nPlease Try again ...')

        else :
            len_ = len(data)
            counter = 0
            desc = ''
            for manga in data :
                counter += 1
                desc += str(counter)+')'+str(manga['attributes']['canonicalTitle'])+'\n'
                if counter == 5 :
                    break

            reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','▶️']
            embed = discord.Embed(title='Search results for '+query,color=discord.Color.purple())
            avatar_url = str(self.bot.user.avatar_url)
            embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
            embed.set_footer(text='React on emoji according to the manga you want')
            embed.add_field(name='Page 1',value=desc,inline=False)
            msg = await ctx.send(embed=embed)        
            for reaction in reactions :
                await msg.add_reaction(reaction)
            
            await AnimeMangaUtil.animeMangaList(self.bot,page,ix,len_,embed,data,ctx,msg,reactions,'manga')

    @commands.command(name='mn-trend')
    async def trendManga(self,ctx):
        page = 0
        ix = 0        
        data = await AnimeMangaUtil.trendingAnimeManga(self.bot,'manga')
        if data is None :
            await ctx.send(f'No Manga found')
        elif data == 0:
            await ctx.send(f'API Error \nPlease Try again ...')

        else :
            len_ = len(data)
            counter = 0
            desc = ''
            for manga in data :
                counter += 1
                desc += str(counter)+')'+str(manga['attributes']['canonicalTitle'])+'\n'
                if counter == 5 :
                    break

            reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','▶️']
            embed = discord.Embed(title='Trending Anime',color=discord.Color.purple())
            avatar_url = str(self.bot.user.avatar_url)
            embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
            embed.set_footer(text='React on emoji according to the manga you want')
            embed.add_field(name='Page 1',value=desc,inline=False)
            msg = await ctx.send(embed=embed)        
            for reaction in reactions :
                await msg.add_reaction(reaction)
                        
            await AnimeMangaUtil.animeMangaList(self.bot,page,ix,len_,embed,data,ctx,msg,reactions,'manga')

def setup(bot):
    bot.add_cog(Manga(bot))

