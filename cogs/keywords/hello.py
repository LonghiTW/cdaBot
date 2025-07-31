from discord.ext import commands

class HelloResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if "你好" in message.content:
            await message.channel.send("你好你好！👋")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(HelloResponder(bot))
