@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "你好" in message.content:
        await message.channel.send("你好你好！👋")

    await bot.process_commands(message)  # 很重要，否則指令不會觸發！
