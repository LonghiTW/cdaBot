import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()  # 載入本地 .env
TOKEN = os.getenv("BOT_TOKEN")  # 從環境變數取得 Token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 遞迴自動載入所有 cogs
def load_all_cogs(bot, folder="cogs"):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                ext = os.path.join(root, file).replace("/", ".").replace("\\", ".").replace(".py", "")
                try:
                    bot.load_extension(ext)
                    print(f"✅ Loaded: {ext}")
                except Exception as e:
                    print(f"❌ Failed to load {ext}: {e}")

@bot.event
async def on_ready():
    print("Bot is ready!")
	print(f"Logged in as {bot.user}")

load_all_cogs(bot)
bot.run(TOKEN)
