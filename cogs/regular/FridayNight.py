from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from astral.sun import sun
from astral import LocationInfo
import pytz


class FridayNight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        self.tz = pytz.timezone("Asia/Taipei")
        self.channel_id = 1099128587220697149
        self.city = LocationInfo("Taipei", "Taiwan", "Asia/Taipei", 25.0330, 121.5654)

        self.schedule_next_friday()
        self.scheduler.start()

    def schedule_next_friday(self):
        today = datetime.now(self.tz).date()
        # 找出本週或下週五
        days_ahead = (4 - today.weekday()) % 7  # 星期五 = 4
        next_friday = today + timedelta(days=days_ahead)
        
        # 計算該天日落時間
        s = sun(self.city.observer, date=next_friday, tzinfo=self.tz)
        target_time = s["sunset"] + timedelta(minutes=1)

        # 如果今天是星期五但時間已過，排下週
        if target_time < datetime.now(self.tz):
            next_friday += timedelta(days=7)
            s = sun(self.city.observer, date=next_friday, tzinfo=self.tz)
            target_time = s["sunset"] + timedelta(minutes=1)

        self.scheduler.add_job(self.send_gif, trigger=DateTrigger(run_date=target_time, timezone=self.tz))
        print(f"✅ 已排程星期五晚上在 {target_time.strftime('%Y-%m-%d %H:%M:%S')} 傳送 gif")

    async def send_gif(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send("https://cdn.discordapp.com/attachments/1298824829633564714/1400393437366194246/image0.gif")
            print("✅ 已成功發送 gif")
        else:
            print("❌ 無法取得頻道")

        # 發送完畢後排下週
        self.schedule_next_friday()

    async def cog_unload(self):
        self.scheduler.shutdown(wait=False)

async def setup(bot):
    await bot.add_cog(FridayNight(bot))
