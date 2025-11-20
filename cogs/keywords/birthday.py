from discord.ext import commands
import datetime
import random

class BirthdayResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # {guild_id: date} → 紀錄今天是否已經觸發過
        self.last_trigger_date = {}

        # 關鍵字
        self.keywords = ["生日", "birthday", "hbd"]

        # 回覆
        self.replies = [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFqfCfC1u-9ZNfWQi4MR3AJGWaRFggbOQwK5yX0BNUk2kbcSnecnd_nN4&s=10",
            "https://megapx-assets.dcard.tw/images/be86cb9c-92d3-4a47-8ee8-c3421bd74579/orig.jpeg",
            "https://media.discordapp.net/attachments/1298824829633564714/1440952723708051507/image0.gif?ex=6920074c&is=691eb5cc&hm=483d4b3dfabf64fd2ddabbe884fff48f37bf7223e9ab127ef2829c912ddb85ab&=&width=747&height=735"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content
        today = datetime.date.today()

        # 如果不是伺服器訊息就忽略
        if message.guild is None:
            return

        guild_id = message.guild.id

        # 一天只觸發一次
        if self.last_trigger_date.get(guild_id) == today:
            return

        # 關鍵字判斷
        if any(keyword in content for keyword in self.keywords):
            # 記錄今天已觸發
            self.last_trigger_date[guild_id] = today

            # 隨機回覆
            reply = random.choice(self.replies)
            await message.channel.send(reply)


async def setup(bot):
    await bot.add_cog(BirthdayResponder(bot))
