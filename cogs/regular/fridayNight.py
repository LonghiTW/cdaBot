from discord.ext import commands, tasks
from discord import TextChannel
from datetime import datetime, timedelta
from astral.sun import sun
from astral import LocationInfo
import pytz


class FridayGif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tz = pytz.timezone("Asia/Taipei")
        self.last_sent_date = None
        self.check_time.start()

    def cog_unload(self):
        self.check_time.cancel()

    def get_taipei_sunset(self):
        location = LocationInfo("Taipei", "Taiwan", "Asia/Taipei", 25.0330, 121.5654)
        now = datetime.now(self.tz)
        s = sun(location.observer, date=now.date(), tzinfo=self.tz)
        return s["sunset"]

    @tasks.loop(minutes=1)
    async def check_time(self):
        now = datetime.now(self.tz)
        sunset = self.get_taipei_sunset()

        # 每週五，且在日落後的一分鐘內
        if now.weekday() == 4 and sunset <= now < sunset + timedelta(minutes=1):
            if self.last_sent_date != now.date():
                try:
                    channel_id = 1099128587220697149
                    channel = self.bot.get_channel(channel_id)
                    if channel and isinstance(channel, TextChannel):
                        await channel.send("https://cdn.discordapp.com/attachments/1298824829633564714/1400393437366194246/image0.gif")
                        self.last_sent_date = now.date()
                except Exception as e:
                    print(f"❌ 發送失敗：{e}")

    @check_time.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(FridayGif(bot))
