import discord
from discord import Option
from discord.ext import commands, tasks
from discord.commands import slash_command
import pickle
from datetime import datetime
from PIL import Image
import imagehash
from config import *

server_ids = [SERVER_ID]

with open('stats.pickle', 'rb') as f:
  data = pickle.load(f)


class Memes(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener('on_message')
  async def new_meme(self, message):
    if message.channel.id == CHANNEL_MEMES and not message.author.bot and \
    len(message.attachments) > 0 or 'https://' in message.content or 'http://' in message.content:
      await message.add_reaction('🤍')
      '''await self.plus(message.author.id)

      files = message.attachments
      if len(files) > 0 and 'image' in files[0].content_type:
          await files[0].save('image.png')
          hash = imagehash.average_hash(Image.open('image.png'))
          if hash in data:
              embed = discord.Embed(colour=discord.Color.red())
              embed.title = '🪗 Баяяяяяяяяяяян'
              embed.description = data[hash]
              await message.reply(embed=embed)
          else:
              data[hash] = message.jump_url
              with open('all_memes.pickle', 'wb') as f:
                  pickle.dump(data, f)'''


def setup(client):
  client.add_cog(Memes(client))
