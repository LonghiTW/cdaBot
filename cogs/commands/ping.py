from discord.ext import commands

# ✅ 設定允許使用指令的頻道 ID 清單
ALLOWED_CHANNELS = {
    1400675645717217350,
    1099128587220697149,
    735692817543987294
}

def is_allowed_channel():
    async def predicate(ctx):
        return ctx.channel.id in ALLOWED_CHANNELS
    return commands.check(predicate)

class PING(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_allowed_channel()  # ✅ 加入頻道限制檢查
    async def ping(self, ctx):
        await ctx.send("pong!")

async def setup(bot):
    await bot.add_cog(PING(bot))
