import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

# 載入 .env 取得兩個 token
load_dotenv()
TOKENS = [
    os.getenv("BOT_TOKEN_CDA"),
    os.getenv("BOT_TOKEN_BTW")
]

# 共用 intents 設定
intents = discord.Intents.default()
intents.message_content = True

# 建立 bot 實例（多個）
bots = [commands.Bot(command_prefix="!", intents=intents) for _ in TOKENS]

# 載入所有 cogs（共用）
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

# 加入事件到每個 bot
for bot in bots:

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print("Bot is ready!")
        print(f"{bot.user}")

# 主函式：啟動所有 bot
async def main():
    await asyncio.gather(*[
        load_all_cogs(bot) for bot in bots
    ])
    await asyncio.gather(*[
        bot.start(token) for bot, token in zip(bots, TOKENS)
    ])

if __name__ == "__main__":
    asyncio.run(main())
