from discord.ext import commands, tasks
from discord import TextChannel
from datetime import datetime, timedelta
from astral.sun import sun
from astral import LocationInfo
import pytz

class FridayGif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gif_sent_today = False
        self.check_time.start()

    def cog_unload(self):
        self.check_time.cancel()

    def get_taipei_sunset(self):
        location = LocationInfo("Taipei", "Taiwan", "Asia/Taipei", 25.0330, 121.5654)
        s = sun(location.observer, date=datetime.now(pytz.timezone("Asia/Taipei")))
        return s["sunset"]

    @tasks.loop(minutes=1)
    async def check_time(self):
        now = datetime.now(pytz.timezone("Asia/Taipei"))
        sunset = self.get_taipei_sunset()

        # 每週五，且在日落後的一分鐘內觸發
        if now.weekday() == 4 and sunset <= now < sunset + timedelta(minutes=1):
            if not self.gif_sent_today:
                try:
                    channel_id = 1099128587220697149
                    channel = self.bot.get_channel(channel_id)
                    if isinstance(channel, TextChannel):
                        await channel.send("https://cdn.discordapp.com/attachments/1298824829633564714/1400393437366194246/image0.gif?ex=688c7985&is=688b2805&hm=a1f3e758cb03c6d989a2865bdb938f1b9ba1eed7db270b756bfc0afca7aaf67a&")
                        self.gif_sent_today = True
                except Exception as e:
                    print(f"❌ 發送失敗：{e}")

        # 過了午夜重置 flag
        if now.hour == 0 and now.minute == 0:
            self.gif_sent_today = False

    @check_time.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(FridayGif(bot))
