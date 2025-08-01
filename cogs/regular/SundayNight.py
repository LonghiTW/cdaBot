from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

class SundayNight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1099128587220697149  # 替換成你要發送的頻道 ID

        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        self.scheduler.add_job(self.send_image, CronTrigger(
            day_of_week='sun',  # 星期日
            hour=21,
            minute=0
        ))
        self.scheduler.start()

    async def send_image(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            try:
                await channel.send(
                    "https://cdn.discordapp.com/attachments/886936474723950611/1396476771377086474/image0.jpg?ex=688d6317&is=688c1197&hm=fda80ec9188732e461b8c478e7fab2bd95e896b06f693454f2adcca50964c339&"
                )
                print("✅ 已在星期日晚上 21:00 發送圖片")
            except Exception as e:
                print(f"❌ 發送圖片失敗：{e}")
        else:
            print("❌ 找不到指定的頻道。")

    async def cog_unload(self):
        self.scheduler.shutdown()

async def setup(bot):
    await bot.add_cog(SundayNight(bot))
