from discord.ext import commands

class IP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ip(self, ctx):
        await ctx.send("`bte.ntc.im`")

async def setup(bot):
    await bot.add_cog(IP(bot))
