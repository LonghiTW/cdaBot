from discord.ext import commands

class ip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ip(self, ctx):
        await ctx.send("`bte.ntc.im`")

def setup(bot):
    bot.add_cog(ip(bot))
