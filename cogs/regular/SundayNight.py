from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import TextChannel
import pytz

class SundayReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        self.channel_id = 1099128587220697149

        # 每週日 21:00 發送
        self.scheduler.add_job(self.send_sunday_image, CronTrigger(
            day_of_week='sun', hour=21, minute=0, timezone=pytz.timezone("Asia/Taipei")
        ))
        self.scheduler.start()

    async def send_sunday_image(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel and isinstance(channel, TextChannel):
            await channel.send("https://cdn.discordapp.com/attachments/886936474723950611/1396476771377086474/image0.jpg")
            print("✅ 已於週日 21:00 傳送圖片")
        else:
            print("❌ 找不到頻道或頻道錯誤")

    async def cog_unload(self):
        self.scheduler.shutdown(wait=False)

async def setup(bot):
    await bot.add_cog(SundayReminder(bot))
