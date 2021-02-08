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

async def searchAnimeMangaDesc(bot,query,type_):
    query = query.strip()
    try :
        async with bot.aioSession.get('https://kitsu.io/api/edge/'+type_+'?filter[text]='+query) as response :
            res = await response.json()  
            if response.status != 200 :
                return 0
            
            for key in res.keys():
                if key == 'errors':
                    return 0
            if len(res['data']) == 0 :
                return None          
            
            return res['data']                

    except Exception as err :
        print(err)

async def trendingAnimeManga(bot,type_):
    try :
        async with bot.aioSession.get('https://kitsu.io/api/edge/trending/'+type_) as response :
            res = await response.json()                       
            if response.status != 200 :
                return None

            for key in res.keys():
                if key == 'errors':
                    return 0
            if len(res['data']) == 0 :
                return None          
            
            return res['data']                

    except Exception as err :
        print(err)

async def genreList(bot,url):
    if url.startswith('/'):
        url = 'https://kitsu.io/api/edge'+url
    try :
        async with bot.aioSession.get(url) as response :
            res = await response.json()
            if response.status != 200 :
                return None
            for key in res.keys():
                if key == 'errors':
                    return 0
            if len(res['data']) == 0 :
                return None          
            
            return res['data']   

    except Exception as err :
        print(err)
        return None

def isNone(var):
    if var is None :
        return '-'
    
    return var

async def animeMangaDetails(bot,data,type_query):
    try :
        type_ = data['type']
        start = data['attributes']['startDate']
        end = data['attributes']['endDate']
        desc = data['attributes']['synopsis']
        title = data['attributes']['canonicalTitle']
        rating = data['attributes']['averageRating']
        status = data['attributes']['status']
        popularityRank = data['attributes']['popularityRank']
        genreUrl = data['relationships']['genres']['links']['related']
        img = data['attributes']['posterImage']['large']

        if genreUrl is not None :        
            genreData = await genreList(bot,genreUrl)
            genre = ''
            if genreData is None :
                genre = '-'
            else :        
                for each in genreData :
                    genre += each['attributes']['name'] + ','

                genre = genre[:-1]
        else :
            genre = ''

        if status == 'current' :
            status = 'ongoing'

        end = isNone(end)
        start = isNone(start)
        status = isNone(status)
        popularityRank = isNone(popularityRank)
        type_ = isNone(type_)

        if rating is None :
            rating = '-'
        else :
            rating = str(round(float(rating) / 10,1))
        

        synopsis = ''
        youtubeUrl = ''
        if desc is not None :
            for c in desc :
                if c == '[' or c == '(':
                    break
                if c == '\n':
                    continue
                synopsis += c
        
        
        embed = discord.Embed(title=title,description=synopsis,color=discord.Color.purple())
        avatar_url = str(bot.user.avatar_url)
        embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
        if img is not None :                            
            embed.set_image(url=img)
        embed.add_field(name='Rating '+':star2:',value=rating,inline=True) 
        embed.add_field(name='Popularity Rank '+':crown:',value=popularityRank,inline=True)
        embed.add_field(name='Genre '+':crossed_swords: :guitar: :ramen: :martial_arts_uniform: :couple_with_heart_woman_man: :stuffed_flatbread: :soccer:',value=genre,inline=False)
        embed.add_field(name='Start Date '+':calendar:',value=start,inline=True)  
        embed.add_field(name='End Date '+':calendar:',value=end,inline=True)  
        embed.add_field(name='Type '+':kimono:',value=type_,inline=True)
        embed.add_field(name='Status '+':woman_with_veil:',value=status,inline=True)
        embed.set_footer(text='Developed by Gnitch#0161')
        if type_query == 'anime':
            episodes = data['attributes']['episodeCount']
            youtubeId = data['attributes']['youtubeVideoId']
            duration = data['attributes']['episodeLength']
            episodes = isNone(episodes)
            duration = isNone(duration)              
            if youtubeId is not None :
                youtubeUrl = 'https://www.youtube.com/watch?v='+youtubeId            
                embed.url = youtubeUrl                        
            embed.add_field(name='Episodes '+':1234:',value=episodes,inline=True)
            embed.add_field(name='Duration '+':stopwatch:',value=str(duration)+' min',inline=True)        
        else :
            chapters = data['attributes']['chapterCount']
            chapters = isNone(chapters)
            volumes = data['attributes']['volumeCount']            
            volumes = isNone(volumes)
            embed.add_field(name='Chapters '+':1234:',value=chapters,inline=True)
            embed.add_field(name='Volumes '+':1234:',value=volumes,inline=True)            
        
        return embed
    
    except Exception as err:
        print(err)

async def animeMangaList(bot,page,ix,len_,embed,data,ctx,msg,reactions,type_):
    def check(reaction, user):
        if user == ctx.author and user != bot.user:
            if(str(reaction.emoji) == '◀️' or '1️⃣' or '2️⃣' or '3️⃣' or '4️⃣' or '5️⃣' or '▶️'):
                return True

        return False

    try :
        reaction, _ = await bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == '▶️':
            page += 1
            ix += 5
            if len_ > ix :
                embed.clear_fields()
                counter = 0
                desc = ''
                for i in range(ix,len_) :
                    counter += 1
                    desc += str(counter)+')'+str(data[i]['attributes']['canonicalTitle'])+'\n'
                    if counter == 5 :
                        break

                embed.add_field(name='Page '+str(page+1),value=desc,inline=False)  
                await msg.edit(embed=embed)                
                await msg.remove_reaction('▶️', ctx.author) 
                for react in reactions :
                    await msg.remove_reaction(react,bot.user)                                               
                                        
                if page >= 1 : 
                    reacts = ['◀️','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']                                  
                    for react in reacts :
                        await msg.add_reaction(react)                                                                  
                else :
                    for react in reactions :
                        await msg.add_reaction(react) 
                
                reaction, _ = await bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == '◀️':
            if ix > 0 :
                ix -= 5
            else :
                ix = 0

            if page > 0 :
                page -= 1
            else :
                page = 0

            len_ = len(data)
            if len_ > ix and ix >= 0 :
                embed.clear_fields()
                counter = 0
                desc = ''
                for i in range(ix,len_) :
                    counter += 1
                    desc += str(counter)+')'+str(data[i]['attributes']['canonicalTitle'])+'\n'
                    if counter == 5 :
                        break

                embed.add_field(name='Page '+str(page+1),value=desc,inline=False)  
                await msg.edit(embed=embed)
                await msg.remove_reaction('◀️', ctx.author) 
                for react in reactions :
                    await msg.remove_reaction(react,bot.user)  

                for react in reactions :
                    await msg.add_reaction(react) 

                reaction, _ = await bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == '1️⃣':
            if(ix < len_):
                embed =  await animeMangaDetails(bot,data[ix+0],type_)
                await ctx.send(embed=embed)
                await msg.delete()

        if str(reaction.emoji) == '2️⃣':
            if(ix+1 < len_):
                embed =  await animeMangaDetails(bot,data[ix+1],type_)
                await ctx.send(embed=embed)
                await msg.delete()

        if str(reaction.emoji) == '3️⃣':
            if(ix+2 < len_):
                embed =  await animeMangaDetails(bot,data[ix+2],type_)
                await ctx.send(embed=embed)
                await msg.delete()

        if str(reaction.emoji) == '4️⃣':
            if(ix+3 < len_):
                embed =  await animeMangaDetails(bot,data[ix+3],type_)
                await ctx.send(embed=embed)
                await msg.delete()

        if str(reaction.emoji) == '5️⃣':
            if(ix+4 < len_):
                embed =  await animeMangaDetails(bot,data[ix+4],type_)
                await ctx.send(embed=embed)                                                            
                await msg.delete()
    
    except Exception as err :
        print(err)

async def searchAnimeSchedule(bot,query):
    try :
        async with bot.aioSessionMy.get('https://evening-everglades-22866.herokuapp.com/api/airing_anime/'+str(query)) as response :
            res = await response.json()  
            if response.status != 200 :
                return None                  
        return res                

    except Exception as err :
        print(err)

