from discord.ext import commands
import datetime
import random

class HelloResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # 每日觸發紀錄
        self.last_trigger_date = {}

        # 中文關鍵字
        self.zh_keywords = ["你好", "大家好"]

        # 英文關鍵字（不分大小寫）
        self.en_keywords = ["hello", "hi"]

        # 英文正則
        self.en_patterns = [
            re.compile(rf"\b{kw}[.!?~]?\b", re.IGNORECASE)
            for kw in self.en_keywords
        ]
        
        # 中文回覆組
        self.replies_zh = [
            "你好你好！👋",
            "https://i.ytimg.com/vi/XwM4ZRSiXv0/hqdefault.jpg"
        ]

        # 英文回覆組
        self.replies_en = [
            "Hello!",
            "Hi there! 👋"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content
        lowered = content.lower()
        today = datetime.date.today()
        channel_id = message.channel.id

        # 一天只觸發一次
        if self.last_trigger_date.get(channel_id) == today:
            return

        # --------------------
        # 中文關鍵字觸發
        # --------------------
        if any(keyword in content for keyword in self.zh_keywords):
            self.last_trigger_date[channel_id] = today
            reply = random.choice(self.replies_zh)
            await message.channel.send(reply)
            return

        # --------------------
        # 英文關鍵字觸發
        # --------------------
        if any(pattern.search(content) for pattern in self.en_patterns):
            self.last_trigger_date[channel_id] = today
            reply = random.choice(self.replies_en)
            await message.channel.send(reply)
            return

async def setup(bot):
    await bot.add_cog(HelloResponder(bot))
