import discord
from discord import Option, SelectOption
from discord.ext import commands, tasks
from discord.commands import slash_command
from discord.ui import View, Select, Button
from config import *
import sqlalchemy as sq
import datetime

server_ids = [SERVER_ID]

db = sq.create_engine(DATABASE_URI)
con = sq.engine.connect()

msg_debt = {}
meme_debt = {}
vc_debt = {}
cur_date = datetime.date.today()

class Economics(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  def db_check(self, id):
    db_object.execute(f"SELECT id FROM users WHERE id = {id}")
    result = db_object.fetchone()
    if not result:
      db.insert().values(id=id, balance=0, limit_hour=0, limit_day=0, rew_row=0, rew_today=False)

  def db_give(self, id, amount):
    self.db_check(id)
    db_object.execute(f"UPDATE users SET money = money + {amount} WHERE id = {id}")
    db_connection.commit()

  def db_get(self, id):
    self.db_check(id)
    db_object.execute(f"SELECT money FROM users WHERE id = {id}")
    return db_object.fetchone()[0]

  def db_daily_get(self, id):
    self.db_check(id)
    db_object.execute(f"SELECT today FROM users WHERE id = {id}")
    if db_object.fetchone()[0] == True:
      return None
    db_object.execute(f"UPDATE users SET today = True WHERE id = {id}")
    db_object.execute(f"SELECT streak FROM users WHERE id = {id}")
    added = int(50 + db_object.fetchone()[0] * 5)
    db_object.execute(f"UPDATE users SET streak = streak + 1 WHERE id = {id}")
    self.db_give(id, added)
    return added

  def db_daily_reset(self):
    db_object.execute('SELECT * FROM users')
    for id, money, streak, today in db_object.fetchall():
      if streak == 7 or today == False:
        db_object.execute(f"UPDATE users SET streak = 1 WHERE id = {id}")
      db_object.execute(f"UPDATE users SET today = False WHERE id = {id}")


  @slash_command(name='balance', description='Узнать баланс', server_ids=server_ids)
  async def balance(self, ctx,
    user: Option(discord.User, 'Не обязательно', required=False)
  ):
    if not user:
      user = ctx.interaction.user
    embed = discord.Embed(colour=discord.Color.gold())
    embed.set_author(name=user.nick if user.nick else user.name, icon_url=user.display_avatar.url)
    embed.title = f'🪙 Баланс: {self.db_get(user.id)}'
    await ctx.respond(embed=embed)

  @slash_command(name='leaderboard', description='Узнать баланс', server_ids=server_ids)
  @commands.has_permissions(administrator=True)
  async def leaderboard(self, ctx,
    user: Option(discord.User, 'Не обязательно', required=False)
  ):
    if not user:
      user = ctx.interaction.user
    embed = discord.Embed(colour=discord.Color.gold())
    embed.set_author(name=user.nick if user.nick else user.name, icon_url=user.display_avatar.url)
    embed.title = f'🪙 Баланс: 💵 {self.db_get(user.id)}'
    await ctx.respond(embed=embed)

  @slash_command(name='send', description='Отправить кому-то деньги', server_ids=server_ids)
  async def pay(self, ctx,
    user: Option(discord.User, 'Кому отправить деньги', required=True),
    amount: Option(int, 'Сколько денег отправить', required=True),
  ):
    if amount < 0:
      embed = discord.Embed(colour=discord.Color.red())
      embed.title = f'🤔 Тут так не работает'
      embed.description = f'Ты не можешь спиздить у кого-то деньги'
    elif self.db_get(ctx.interaction.user.id) >= amount:
      self.db_give(ctx.interaction.user.id, -amount)
      self.db_give(user.id, amount)
      embed = discord.Embed(colour=discord.Color.gold())
      embed.title = f'💸 Симп потратил {amount}'
      embed.description = f'От {ctx.interaction.user.mention} к {user.mention}'
    else:
      embed = discord.Embed(colour=discord.Color.red())
      embed.title = f'📉 Денег мала'
      embed.description = f'Баланс: **{self.db_get(ctx.interaction.user.id)}** 🪙\nПеревод: **{amount}** 🪙'
    await ctx.respond(embed=embed)


  @slash_command(name='shop', description='Магазин сервера', server_ids=server_ids)
  @commands.has_permissions(administrator=True)
  async def shop(self, ctx):
    embed = discord.Embed(colour=discord.Color.gold())
    embed.title = f'🛍️ Магазин сервера\n⠀'
    embed.set_footer(text='⠀\nВсе условия обговраиваются с админом. Он имеет право отказаться и вернуть деньги')

    select = Select(min_values=1, max_values=1, placeholder='Выбери, чтобы купить')
    for item in SHOP_ITEMS:
      embed.add_field(name=f'{item.name} - {item.price} 🪙', value=item.desc + '\n', inline=False)
      select.add_option(label=item.name, description=str(item.price))

    async def shop_callback(interaction):
      item = None
      for item in SHOP_ITEMS:
        if item.name == select.values[0]:
          break
      balance = self.db_get(interaction.user.id)
      if balance >= item.price:
        self.db_give(interaction.user.id, -item.price)
        buy_embed = discord.Embed(colour=discord.Color.gold())
        buy_embed.title = '🛒 Покупка'
        buy_embed.description = f'**{item.name}**\n{item.desc}\n__Напиши сюда свои пожелания, я скоро отвечу__'
        buy_embed.set_footer(text=f'Баланс: **{balance}** 🪙')
        await interaction.user.send(embed=buy_embed)

        log_embed = discord.Embed(colour=discord.Color.gold())
        log_embed.title = '🛒 Покупка'
        log_embed.description = f'{interaction.user.mention} купил **{item.name}**'
        channel = self.bot.get_channel(CHANNEL_GOSHIK)
        await channel.send(embed=log_embed)
      else:
        buy_embed = discord.Embed(colour=discord.Color.red())
        buy_embed.title = f'📉 Денег мала'
        buy_embed.description = f'Баланс: **{balance}** 🪙\nНужно: **{item.price}** 🪙'
        await interaction.user.send(embed=buy_embed)

    select.callback = shop_callback
    view = View()
    view.add_item(select)
    await ctx.respond(embed=embed, view=view)


  @slash_command(name='daily', description='Ежедневная награда', server_ids=server_ids)
  @commands.has_permissions(administrator=True)
  async def daily(self, ctx):
    response = self.db_daily_get(ctx.interaction.user.id)
    if response == None:
      embed = discord.Embed(colour=discord.Color.red())
      embed.title = '📛 Ты сегодня уже получал награду'
      embed.set_footer(text='- хитрый пидорас', icon_url=ctx.interaction.user.display_avatar.url)
    else:
      embed = discord.Embed(colour=discord.Color.gold())
      embed.title = f'📅 Ежедневная награда: {response}'
      embed.description = f'Баланс: **{self.db_get(ctx.interaction.user.id)}**'
    await ctx.respond(embed=embed)


  @slash_command(name='ec-add', description='Добавить деньги', server_ids=server_ids)
  @commands.has_permissions(administrator=True)
  async def ec_add(self, ctx,
    user: Option(discord.User, 'У кого менять баланс', required=True),
    amount: Option(int, 'На сколько изменить баланс', required=True),
  ):
    self.db_give(user.id, amount)
    embed = discord.Embed(colour=discord.Color.gold())
    embed.set_author(name=user.nick if user.nick else user.name, icon_url=user.display_avatar.url)
    embed.title = f'🪙 Баланс изменён на {"+" if amount > 0 else ""}{amount}'
    embed.description = f'Новый баланс: **{self.db_get(user.id)}** 🪙'
    await ctx.respond(embed=embed)

  @slash_command(name='ec-update', description='Обновить балансы', server_ids=server_ids)
  @commands.has_permissions(administrator=True)
  async def ec_update(self, ctx):
    await self.give_debt()
    self.db_daily_reset()
    embed = discord.Embed(colour=discord.Color.gold())
    embed.title = f'🪙 Баланс был обновлён'
    await ctx.respond(embed=embed)


  @tasks.loop(hours=1)
  async def give_debt(self):
    global msg_debt, meme_debt, vc_debt
    for debt in [msg_debt, meme_debt, vc_debt]:
      for id in debt:
        self.db_give(id, debt[id])
    msg_debt = {}
    meme_debt = {}
    vc_debt = {}

  @tasks.loop(minutes=5)
  async def give_vc_debt(self):
    global vc_debt, cur_date
    for channel in self.bot.get_channel(VC_START).category.voice_channels:
      if len(channel.members) < 2:
        continue
      for member in channel.members:
        if not member.voice.self_mute and not member.voice.self_deaf:
          if member.id not in vc_debt:
            vc_debt[member.id] = 0
          vc_debt[member.id] = min(vc_debt[member.id] + MONEY_FOR_VC, MONEY_MAX_VC)

    if datetime.date.today() != cur_date:
      db_object.execute("")
      cur_date.datetime.date.today()


  @commands.Cog.listener('on_ready')
  async def is_ready(self):
    self.give_debt.start()
    self.give_vc_debt.start()


  @commands.Cog.listener('on_message')
  async def new_message(self, message):
    global msg_debt, meme_debt
    if message.channel.id == CHANNEL_MEMES and not message.author.bot and \
    (len(message.attachments) > 0 or 'https://' in message.content or 'http://' in message.content):
      await message.add_reaction('🤍')
      if message.author.id not in meme_debt:
        meme_debt[message.author.id] = 0
      meme_debt[message.author.id] = min(meme_debt[message.author.id] + MONEY_FOR_MEME, MONEY_MAX_MEME)
      return
    if message.author.id not in msg_debt:
      msg_debt[message.author.id] = 0
    msg_debt[message.author.id] = min(msg_debt[message.author.id] + MONEY_FOR_MSG, MONEY_MAX_MSG)


  @slash_command(name='rps', description='Камень, ножницы, бумага', server_ids=server_ids)
  @commands.has_permissions(administrator=True)
  async def rps(self, ctx,
    ставка: Option(int, 'Можно НЕ играть на деньги', required=False),
  ):
    if ставка and ставка < self.db_get(ctx.interaction.user.id):
      buy_embed = discord.Embed(colour=discord.Color.red())
      buy_embed.title = f'📉 Денег мала'
      buy_embed.description = f'Баланс: **{self.db_get(ctx.interaction.user.id)} 🪙**\nНужно: **{ставка}** 🪙'
      await ctx.respond(embed=buy_embed)
      return

    embed = discord.Embed(colour=discord.Color.fuchsia())
    embed.title = f'👊🖐️✌️ Камень ножницы бумага'
    if ставка:
      embed.description = f'Ставка: **{ставка}** 🪙'
    embed.set_footer(text='Каждый игрок должен нажать одну кнопку')

    view = View()

    async def rps_callback(interaction):
      print(interaction.data)

    view.add_item(Button(emoji='👊', label='Камень', callback=rps_callback, custom_id='rock'))
    view.add_item(Button(emoji='✌️', label='Ножницы', callback=rps_callback, custom_id='paper'))
    view.add_item(Button(emoji='🖐️', label='Бумага', callback=rps_callback, custom_id='scissors'))
    await ctx.respond(embed=embed, view=view)


def setup(bot):
  bot.add_cog(Economics(bot))
