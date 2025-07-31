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
        self.channel_id = 1099128587220697149  # ✅ 替換為你要發送的頻道 ID
        self.tz = pytz.timezone("Asia/Taipei")

        # 建立 Astral 地點（台北）
        self.city = LocationInfo("Taipei", "Taiwan", "Asia/Taipei", 25.0330, 121.5654)

        # 初始化排程器
        self.scheduler = AsyncIOScheduler(timezone=self.tz)

        # ➤ 啟動時立即安排今日任務
        self.schedule_daily_job()

        # ➤ 每天凌晨 2 點重新安排一次
        self.scheduler.add_job(self.schedule_daily_job, CronTrigger(hour=2, minute=0, timezone=self.tz))
        self.scheduler.start()

    def get_sunset_minus_offset(self, date):
        """取得指定日期日落時間 - 1小時40分"""
        s = sun(self.city.observer, date=date, tzinfo=self.city.timezone)
        return s['sunset'] - timedelta(hours=1, minutes=40)

    def schedule_daily_job(self):
        now = datetime.now(self.tz)
        target_time = self.get_sunset_minus_offset(now.date())

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
            id=f"sunset_notice_{target_time.date()}",
            replace_existing=True
        )
        print(f"✅ 日落前 1 小時 40 分通知安排於：{target_time.strftime('%Y-%m-%d %H:%M:%S')}")

    async def send_sunset_message(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send("☀️ 現在是日落前 1 小時 40 分，準備收工囉！")
        else:
            print("❌ 找不到指定頻道！")



async def setup(bot):
    await bot.add_cog(SunsetNotifier(bot))
