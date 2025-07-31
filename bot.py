import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

# 載入本地 .env
load_dotenv()  
TOKEN = os.getenv("BOT_TOKEN")  # 從環境變數取得 Token

# 建立 intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 bot 實例
bot = commands.Bot(command_prefix="!", intents=intents)

# 遞迴自動載入所有 cogs
async def load_all_cogs(bot, folder="cogs"):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                ext = os.path.join(root, file).replace("/", ".").replace("\\", ".").replace(".py", "")
                try:
                    await bot.load_extension(ext)
                    print(f"✅ Loaded: {ext}")
                except Exception as e:
                    print(f"❌ Failed to load {ext}: {e}")

# 處理文字訊息：讓 listener 接管 + 指令
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 呼叫所有 @Cog.listener()
    await bot.process_commands(message)

# 當 bot 上線時
@bot.event
async def on_ready():
    print("Bot is ready!")
    print(f"Logged in as {bot.user}")

# 主執行函式（用 asyncio.run 執行 async 流程）
async def main():
    await load_all_cogs(bot)
    await bot.start(TOKEN)

# 執行 bot
if __name__ == "__main__":
    asyncio.run(main())
