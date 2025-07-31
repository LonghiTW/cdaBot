import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from astral.sun import sun
from astral import LocationInfo
import pytz

class SunsetNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        self.channel_id = 1099128587220697149

        self.city = LocationInfo("Taipei", "Taiwan", "Asia/Taipei", 25.0330, 121.5654)
        self.tz = pytz.timezone("Asia/Taipei")

        # 每天凌晨 2 點安排行程
        self.scheduler.add_job(self.schedule_daily_job, CronTrigger(hour=2, minute=0, timezone=self.tz))
        self.scheduler.start()

    def get_sunset_minus_1h40m(self, date):
        s = sun(self.city.observer, date=date, tzinfo=self.tz)
        return s['sunset'] - timedelta(hours=1, minutes=40)

    def schedule_daily_job(self):
        now = datetime.now(self.tz)
        target_time = self.get_sunset_minus_1h50m(now.date())

        self.scheduler.add_job(
            self.send_sunset_message,
            trigger=CronTrigger(
                year=target_time.year,
                month=target_time.month,
                day=target_time.day,
                hour=target_time.hour,
                minute=target_time.minute,
                timezone=self.tz
            ),
            id=f"sunset_message_{target_time.date()}",  # 防止重複排程
            replace_existing=True
        )
        print(f"✅ 日落前 1 小時 50 分任務已安排於：{target_time.strftime('%Y-%m-%d %H:%M:%S')}")

    async def send_sunset_message(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send("☀️ 現在是日落前 1 小時 50 分，準備收工囉！")
            print("📤 已發送日落提醒訊息。")
        else:
            print("❌ 找不到指定頻道。")

async def setup(bot):
    await bot.add_cog(SunsetNotifier(bot))
