import discord
from discord.commands import (slash_command)
from config import *

bot = discord.Bot(intents=discord.Intents.all())

cogs = [
    'admin',
    'fun_commands',
    'roles',
    'voice',
]
for cog in cogs:
    bot.load_extension('cogs.' + cog)


@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_GOSHIK)
    await channel.send('I\'m ready')
    print('Bot is ready')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=BOT_STATUS))


bot.run(TOKEN)
