import discord
from discord.ext import commands
import os

class Admin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def cog_before_invoke(self, ctx):
        admin = await self.bot.is_owner(ctx.author)
        if not admin:
            raise commands.CommandInvokeError("Only admin is allowed to use this command")
        return admin

    @commands.command(name='reload')
    async def reload(self, ctx):
        try:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.bot.unload_extension(f'cogs.{filename[:-3]}') 
                    self.bot.load_extension(f'cogs.{filename[:-3]}') 
        except Exception as err :
            # print(f'Reloading failed of Cog {filename[:-3]}, Error: {err}')
            await ctx.send(f'Reloading failed of Cog {filename[:-3]}, Error: {err}')
        else :
            await ctx.send(f'```Bot updated succesfully```')

def setup(bot):
    bot.add_cog(Admin(bot))
