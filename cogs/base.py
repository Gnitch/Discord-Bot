import discord
from discord.ext import commands
import time

class Base(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help',aliases=['h'])
    async def help(self, ctx):
        embed = discord.Embed(title='Bot for weebs !!',description='My prefix is `/`',color=discord.Color.purple())
        avatar_url = str(self.bot.user.avatar_url)
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
        embed.add_field(name='/ping',value="Bot's Latency",inline=True)         
        embed.add_field(name='/help-anime',value="Anime commands",inline=True)         
        embed.add_field(name='/help-manga',value="Manga commands",inline=True)         
        embed.add_field(name='/help-fun',value="Fun commands",inline=True)                 
        embed.set_footer(text='Developed by Gnitch#0161🌸')
        try :
            await ctx.send(embed=embed)
        except Exception :
            await ctx.send('Permissions for embed is not given')
    
    @commands.command(name='help-anime')
    async def helpAnime(self, ctx):
        embed = discord.Embed(title='Anime commands!!',color=discord.Color.purple())
        avatar_url = str(self.bot.user.avatar_url)
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)
        embed.add_field(name='/anime [anime-name]',value="Search for anime",inline=True)        
        embed.add_field(name='/an-trend',value="Top 10 trending anime",inline=True)
        embed.add_field(name='/an-schedule [day number(1-7)]',value="Anime Schedule of a particular day \n Eg. `/an-schedule 1` (to recieve schedule of monday)",inline=False)
        embed.add_field(name='/set [#channel-name]',value="Send Anime schedule of the day to the channel daily",inline=True)
        embed.add_field(name='/an-recommend [anime-name]',value="Get Anime recommendations \n Anime name should be Japanese not English based \neg. nanatsu no Taizai `NOT SEVEN DEADLY SINS`",inline=False)
        embed.set_footer(text='Developed by Gnitch#0161🌸')
        try :
            await ctx.send(embed=embed)
        except Exception :
            await ctx.send('Permissions for embed is not given')

    @commands.command(name='help-manga')
    async def helpManga(self, ctx):
        embed = discord.Embed(title='Manga commands!!',color=discord.Color.purple())
        avatar_url = str(self.bot.user.avatar_url)
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)        
        embed.add_field(name='/manga [manga-name]',value="Search for manga",inline=True)        
        embed.add_field(name='/mn-trend',value="Top 10 trending manga",inline=True)
        embed.add_field(name='/mn-recommend [manga-name]',value="Get Manga recommendations \n Manga name should be Japanese not English based\neg. nanatsu no taizai `NOT SEVEN DEADLY SINS`",inline=False)
        embed.set_footer(text='Developed by Gnitch#0161🌸')        
        try :
            await ctx.send(embed=embed)
        except Exception :
            await ctx.send('Permissions for embed is not given')

    @commands.command(name='help-fun')
    async def helpFun(self, ctx):
        embed = discord.Embed(title='Fun commands!!',color=discord.Color.purple())
        avatar_url = str(self.bot.user.avatar_url)
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(name='Hitagi chan',url='https://discord.com/api/oauth2/authorize?client_id=800964718155005952&permissions=519232&scope=bot',icon_url=avatar_url)        
        embed.add_field(name='/an-meme',value="Random meme from r/goodanimemes",inline=True)
        embed.add_field(name='/wallpaper',value="Random wallpaper from r/AnimeWallpapers",inline=True)
        embed.add_field(name='/quote',value="Sends a random Anime quote",inline=True)
        embed.add_field(name='/waifu [#member-name]',value="Gets a waifu for the member",inline=True)
        embed.set_footer(text='Developed by Gnitch#0161🌸')        
        try :
            await ctx.send(embed=embed)
        except Exception :
            await ctx.send('Permissions for embed is not given')

    @commands.command(name='ping')
    async def ping(self, ctx):     
        ch = await self.bot.fetch_channel(762722885810651166)
        await ch.send('Tets')
        await ctx.send(f'Pong :ping_pong: \n Took `{round(self.bot.latency*1000)}ms`')

def setup(bot):
    bot.add_cog(Base(bot))
