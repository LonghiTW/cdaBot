import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()  # 載入本地 .env（Pterodactyl 中不影響）

TOKEN = os.getenv("BOT_TOKEN")  # 從環境變數取得 Token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command()
async def hello(ctx):
    await ctx.send("你好！我上線了！")

bot.run(TOKEN)
