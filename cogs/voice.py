import discord
from discord.ext import tasks, commands
from config import *


def is_gaming(channel):
  global VC_START
  return channel.id != VC_START and channel.id != VC_AFK

def is_game(activity):
  return isinstance(activity, discord.Game) or isinstance(activity, discord.Activity)


class Voice(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener('on_voice_state_update')
  async def vc_update(self, member, before, after):
    global VC_START
    if before.channel != None and is_gaming(before.channel) and len(before.channel.members) == 0:
      await before.channel.delete()
    if after.channel != None and after.channel.id == VC_START:
      new_name = 'Voice'
      for activity in member.activities:
        if (is_game(activity)):
          new_name = activity.name
          break
      channel = await after.channel.category.create_voice_channel(name = new_name, position = 1)
      await member.move_to(channel)

  @commands.Cog.listener('on_ready')
  async def start_checker(self):
    self.check_sessions.start()

  @tasks.loop(minutes = 4)
  async def check_sessions(self):
    channel_chill = self.bot.get_channel(VC_START)
    for channel in channel_chill.category.voice_channels:
      if not is_gaming(channel):
        continue

      new_name = 'Voice'
      for member in channel.members:
        if member.bot:
          continue
        other = False
        the_same = False
        for activity in member.activities:
          if is_game(activity):
            if new_name == 'Voice':
              new_name = activity.name
            if activity.name == new_name:
              the_same = True
            else:
              other = True
        if not the_same and other:
          new_name = 'Voice'
          break

      if channel.name != new_name:
        await channel.edit(name = new_name)


def setup(bot):
  bot.add_cog(Voice(bot))