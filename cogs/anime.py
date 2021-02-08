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
import sys

from utils import AnimeMangaUtil

class Anime(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        # self.postAnimeSchedule.start() #Enable During production
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):           
            await ctx.send('Type `/help` to check correct usage of commands')
            return           

    @commands.command(name='anime',aliases=['an'])
    async def animeSearch(self,ctx, *,query):
        page = 0
        ix = 0  
        data = await AnimeMangaUtil.searchAnimeMangaDesc(self.bot,query,'anime')     
        if data is None or query is None:
            await ctx.send(f'No Anime found')
        elif data == 0:
            await ctx.send(f'API Error \nPlease Try again ...')

        else :
            len_ = len(data)
            counter = 0
            desc = ''
            for anime in data :
                counter += 1
                desc += str(counter)+')'+str(anime['attributes']['canonicalTitle'])+'\n'
                if counter == 5 :
                    break

            reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','▶️']
            embed = discord.Embed(title='Search results for '+query,color=discord.Color.purple())
            avatar_url = str(self.bot.user.avatar_url)
            embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
            embed.set_footer(text='React on emoji according to the anime you want')
            embed.add_field(name='Page 1',value=desc,inline=False)     
            try :
                msg = await ctx.send(embed=embed)
            except Exception :
                await ctx.send('Permissions for embed is not given')
            else :            
                for reaction in reactions :
                    await msg.add_reaction(reaction)
                
                await AnimeMangaUtil.animeMangaList(self.bot,page,ix,len_,embed,data,ctx,msg,reactions,'anime')

    @commands.command(name='an-trend')
    async def trendAnime(self,ctx):
        page = 0
        ix = 0        
        data = await AnimeMangaUtil.trendingAnimeManga(self.bot,'anime')
        if data is None :
            await ctx.send(f'No Anime found')
        elif data == 0:
            await ctx.send(f'API Error \nPlease Try again ...')

        else :
            len_ = len(data)
            counter = 0
            desc = ''
            for anime in data :
                counter += 1
                desc += str(counter)+')'+str(anime['attributes']['canonicalTitle'])+'\n'
                if counter == 5 :
                    break

            reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','▶️']
            embed = discord.Embed(title='Trending Anime',color=discord.Color.purple())
            avatar_url = str(self.bot.user.avatar_url)
            embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
            embed.set_footer(text='React on emoji according to the anime you want')
            embed.add_field(name='Page 1',value=desc,inline=False)
            msg = await ctx.send(embed=embed)        
            try :
                msg = await ctx.send(embed=embed)
            except Exception :
                await ctx.send('Permissions for embed is not given')
            else :             
                for reaction in reactions :
                    await msg.add_reaction(reaction)
                
                
                await AnimeMangaUtil.animeMangaList(self.bot,page,ix,len_,embed,data,ctx,msg,reactions,'anime')

    @commands.command(name='an-schedule')
    async def animeSearchSchedule(self,ctx, *,query): 
        query = query.strip()    
        if int(query) == 6 :
            query = 6   
        try :
            if int(query) not in [1,2,3,4,5,6,7] and type(query) is not int:
                await ctx.send('Incorrext week number specified \n Week number should be in the range 1-7')           

            else :              
                data = await AnimeMangaUtil.searchAnimeSchedule(self.bot,query)
                if data is None :
                    await ctx.send('API Error')
                else :
                    if data['animeList'][-1] == ','  :
                        temp = data['animeList'][:-1]
                        animeNames = temp.split(',')                
                    else :
                        animeNames = data['animeList'].split(',')                

                    if data['timeStampList'][-1] == ','  :
                        temp = data['timeStampList'][:-1]
                        timeStamps = temp.split(',')                
                    else :
                        timeStamps = data['timeStampList'].split(',')                
                    lst = zip(animeNames,timeStamps)
                    embed = discord.Embed(title='Anime Schedule for '+data['day'].capitalize(),color=discord.Color.purple())
                    avatar_url = str(self.bot.user.avatar_url)
                    embed.set_thumbnail(url=avatar_url)                     
                    embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
                    embed.set_footer(text='Developed by Gnitch#0161🌸')                                                    
                    guild_region = ctx.guild.region
                    flag = False
                    if str(guild_region) == 'india' :                                                 
                        flag = True
                    
                    for anime, time in lst :
                        if flag :
                            time = 'will air at ' + time
                        else :
                            time = '-'

                        embed.add_field(name=anime,value=time,inline=True)   
                    try :
                        await ctx.send(embed=embed)
                    except Exception :
                        await ctx.send('Permissions for embed is not given')

                    if not flag :
                        await ctx.send('```To display airing time of a anime set SERVER REGION TO INDIA \n This bot displays airing time of anime according to indian timezone```')
        
        except Exception as err :
            print(err)
            await ctx.send('Incorrext week number specified \n Week number should be in the range 1-7')           

    def dbConnect(self):
        load_dotenv()
        DB_USER = os.getenv('DB_USER')        
        DB_HOST = os.getenv('DB_HOST')        
        DB_PWD = os.getenv('DB_PWD')                
        try :
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_USER,
                user=DB_USER,
                password=DB_PWD,
                port=5432
            )
            return conn

        except psycopg2.Error as err :
            print(err)
            return None


    @commands.command(name='set')
    async def setAnimeSchedule(self,ctx, *,query): 
        try :
            if query[0:2] == '<#' and query[-1] == '>':
                channel = self.bot.get_channel(int(str(query)[2:-1]))
                guild = ctx.guild         
                conn = self.dbConnect()
                if conn is not None :
                    try :
                        conn.set_session(autocommit=True)
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM discord')
                        rows = cur.fetchall()
                        flag = False
                        for row in rows :
                            if row[1] == str(guild.id) and row[2] == str(channel.id):
                                flag = True
                                break
                        
                        if not flag :
                            cur.execute('INSERT INTO discord (guild_id,channel_id) VALUES (%s,%s)',(guild.id,channel.id))
                        else :
                            await ctx.send('Daily schedule is already set')

                    except psycopg2.Error as err :
                        print(err)
                    conn.close()

                if channel.permissions_for(guild.me).send_messages :
                    await channel.send('Anime Schedule will be send in this channel')
                else :
                    await ctx.send('No permission to send message')

            else :
                await ctx.send('Incorrect query specified')
        except Exception as err :
            print(err)        

    @tasks.loop(hours=10.0)
    async def postAnimeSchedule(self):
        now = datetime.now()
        curr_time = now.strftime('%H:%M')
        min_time = now.replace(hour=0, minute=5, second=0, microsecond=0).strftime('%H:%M')
        max_time = now.replace(hour=1, minute=30, second=0, microsecond=0).strftime('%H:%M')
        flag = min_time < curr_time < max_time
        # flag = True
        if flag :
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="with Kanbaru"))    
            guilds = await self.bot.fetch_guilds().flatten()
            conn = self.dbConnect()
            conn.set_session(autocommit=True)
            try :
                cur = conn.cursor()
                cur.execute('SELECT * FROM discord')
                rows = cur.fetchall()
                print(rows)
                lst = zip(guilds,rows)
                for guild, row in lst :
                    if str(guild.id) == str(row[1]):
                        channel = self.bot.get_channel(int(row[2]))
                        if channel is not None :
                            today = date.today()
                            today = calendar.day_name[today.weekday()].lower()
                            data = await AnimeMangaUtil.searchAnimeSchedule(self.bot,today)
                            if data is None :
                                await channel.send('API Error')
                            else :
                                if data['animeList'][-1] == ','  :
                                    temp = data['animeList'][:-1]
                                    animeNames = temp.split(',')                
                                else :
                                    animeNames = data['animeList'].split(',')                

                                if data['timeStampList'][-1] == ','  :
                                    temp = data['timeStampList'][:-1]
                                    timeStamps = temp.split(',')                
                                else :
                                    timeStamps = data['timeStampList'].split(',')                
                                lst = zip(animeNames,timeStamps)
                                embed = discord.Embed(title='Anime Schedule for '+data['day'].capitalize(),color=discord.Color.purple())
                                avatar_url = str(self.bot.user.avatar_url)
                                embed.set_thumbnail(url=avatar_url)                                
                                embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
                                embed.set_footer(text='Developed by Gnitch#0161🌸')                                
                                guild_ = await self.bot.fetch_guild(guild.id)
                                guild_region = guild_.region
                                flag = False
                                if str(guild_region) == 'india' :                                                 
                                    flag = True
                                
                                for anime, time in lst :
                                    if flag :
                                        time = 'will air at ' + time
                                    else :
                                        time = '-'

                                    embed.add_field(name=anime,value=time,inline=True)  
                                try :
                                    await channel.send(embed=embed)
                                except Exception :
                                    await channel.send('Permissions for embed is not given')                                                                                               
                                if not flag :
                                    await channel.send('```To display airing time of a anime set SERVER REGION TO INDIA \n This bot displays airing time of anime according to indian timezone```')

                        else:
                            cur = conn.cursor()
                            cur.execute("DELETE FROM discord WHERE ID ="+str(row[0]))

                    else :
                        cur = conn.cursor()
                        cur.execute("'DELETE FROM discord WHERE ID ="+str(row[0]))
            except (psycopg2.Error,Exception) as err :
                print(err)
            conn.close()

     
def setup(bot):
    bot.add_cog(Anime(bot))

