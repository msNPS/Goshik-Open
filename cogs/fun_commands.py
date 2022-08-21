import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
import random
from config import *

server_ids = [SERVER_ID]


class FunCommands(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


  @slash_command(name='ping', description='Sends bot\'s latency', server_ids=server_ids)
  async def ping(self, ctx):
    embed = discord.Embed(colour=discord.Color.blue())
    embed.title = f'📶 Задержка: {round(self.bot.latency * 1000)} лет'
    await ctx.respond(embed=embed)


  @slash_command(name='ball', description='Магический шар', server_ids=server_ids)
  async def ball(self, ctx,
    вопрос: Option(str, 'Вопрос', required=False)
  ):
    embed = discord.Embed(colour=discord.Color.purple())
    embed.title = '🔮 ' + random.choice(ANSWER_BALL)
    if вопрос != None:
      embed.description = f'Вопрос: {вопрос}'
    await ctx.respond(embed=embed)


  @slash_command(name='ben', description='Говорящий Бэн', server_ids=server_ids)
  async def ben(self, ctx,
    вопрос: Option(str, 'Вопрос', required=False)
  ):
    embed = discord.Embed(colour=discord.Color.dark_orange())
    embed.title = '🐶 ' + random.choice(ANSWER_BEN)
    if вопрос != None:
      embed.description = f'Вопрос: {вопрос}'
    await ctx.respond(embed=embed)


  @slash_command(name='roll', description='Случайное число', server_ids=server_ids)
  async def roll(self, ctx,
    число: Option(int, 'Наибольшое число', required=False)
  ):
    if число == None:
      число = 10
    embed = discord.Embed(colour=discord.Color.dark_blue())
    embed.title = '🔘 Результат: ' + str(random.randint(1, число))
    embed.description = f'Среди чисел от 1 до {str(число)}'
    await ctx.respond(embed=embed)


  @slash_command(name='pick', description='Выбор одного из вариантов', server_ids=server_ids)
  async def pick(self, ctx,
    варианты: Option(str, name='варианты', description='Через запятую', required=True)
  ):
    embed = discord.Embed(colour=discord.Color.dark_teal())
    embed.title = '💠 Результат: ' + str(random.choice(варианты.split(',')))
    embed.description = f'Варианты: {варианты}'
    await ctx.respond(embed=embed)


  @slash_command(name='coin', description='Орёл или решка', server_ids=server_ids)
  async def fun_money(self, ctx):
    embed = discord.Embed(colour=discord.Color.gold())
    embed.title = random.choice(ANSWER_MONEY)
    await ctx.respond(embed=embed)


  '''@bot.slash_command(name='rock', description='Камень, ножницы, бумага', server_ids=server_ids)
  async def rock(self, ctx):
    while True:
      buttons = [
        Components.create_button(label='🗿Камень', style=ButtonStyle.blurple, custom_id='0'),
        Components.create_button(label='✂️Ножницы', style=ButtonStyle.blurple, custom_id='1'),
        Components.create_button(label='🧻Бумага', style=ButtonStyle.blurple, custom_id='2')
      ]
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.title = '👊 Камень, ножницы, бумага'
      embed.description = 'Каждый игрок должен выбрать один из вариантов'
      actionrow = Components.create_actionrow(*buttons)
      await ctx.send(embed=embed, components=[actionrow])

      first = await Components.wait_for_component(self.bot, components=actionrow)
      await first.edit_origin()
      second = await Components.wait_for_component(self.bot, components=actionrow)
      if first.custom_id == second.custom_id:
        embed.title = '👊 __Ничья__'
      elif (first.custom_id=='0' and second.custom_id=='1') or (first.custom_id=='1' and second.custom_id=='2') or (first.custom_id=='2' and second.custom_id=='0'):
        embed.title = f'👊 __{first.author.name}__ победил!'
      else:
        embed.title = f'👊 __{second.author.name}__ победил!'

      embed.description = ''
      buttons = [Components.create_button(label='🔁Заново', style=ButtonStyle.blurple, custom_id='replay')]
      actionrow = Components.create_actionrow(*buttons)
      chooser = {'0': '🗿Камень', '1': '✂️Ножницы', '2': '🧻Бумага'}
      embed.add_field(name=first.author.name+':', value=chooser[first.custom_id], inline=False)
      embed.add_field(name=second.author.name+':', value=chooser[second.custom_id], inline=False)
      await second.edit_origin(embed=embed, components=[actionrow])

      replay = await Components.wait_for_component(self.bot, components=actionrow)
      await replay.edit_origin()'''


def setup(bot):
  bot.add_cog(FunCommands(bot))