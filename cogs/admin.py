import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
from config import *

server_ids = [SERVER_ID]

file_answer_welcome = open('answer_welcome.txt', 'rb')
answer_welcome = file_answer_welcome.read().decode('utf-8')
file_answer_welcome.close()

muted = False


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='clear', description='Удалить последние x сообщений', server_ids=server_ids)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx,
                    amount: Option(int, 'Кол-во сообщений', required=True)
                    ):
        await ctx.respond('...')
        await ctx.channel.purge(limit=amount + 1)

    @slash_command(name='idclear', description='Удалить все сообщение до определённого', server_ids=server_ids)
    @commands.has_permissions(administrator=True)
    async def idclear(self, ctx,
                      id: Option(str, 'ID последнего удалённого',
                                 required=True)
                      ):
        await ctx.respond('...')
        amount = 0
        async for message in ctx.channel.history(limit=None):
            if message.id == int(id):
                break
            amount += 1
        await ctx.channel.purge(limit=amount + 1)

    @slash_command(name='memeclear', description='Очистить не мемы', server_ids=server_ids)
    @commands.has_permissions(administrator=True)
    async def memeclear(self, ctx):
        await ctx.respond('...')
        amount = 0
        async for message in ctx.channel.history(limit=None):
            if len(message.reactions) > 0 and str(message.reactions[0]) == '🤍':
                break
            amount += 1
        await ctx.channel.purge(limit=amount)

    @slash_command(name='sendmessage', description='Отправить сообщение', server_ids=server_ids)
    @commands.has_permissions(administrator=True)
    async def sendmessage(self, ctx,
                          канал: Option(str, 'Канал назначения', required=True),
                          контент: Option(str, 'Текст сообщения', required=True),
                          ):
        target = self.bot.get_user(int(канал))
        if target == None:
            target = self.bot.get_channel(int(канал))
        if target != None and контент != None:
            await target.send(контент)
            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.title = f'📨 \"{контент}\"'
        else:
            embed = discord.Embed(color=discord.Color.red())
            embed.title = '❌ ' + 'Ошибка'
            embed.description = f'Контент: \"{контент}\"'
        embed.set_footer(text=str(канал))
        await ctx.respond(embed=embed)

    '''@slash_command(name='amongus', description='Мьют всех в канале', server_ids=server_ids)
  @commands.has_any_role([ROLE_MUTER])
  async def amongus(self, ctx):
    global muted
    muted = not muted
    if ctx.author.voice.channel != None:
      for member in ctx.author.voice.channel.members:
        await member.edit(mute = muted)

    embed = discord.Embed(color=discord.Color.dark_gray())
    if not muted:
      embed.title = '🔊 Пиздеть можно'
      buttons = [Components.create_button(label='Уебать всех', style=ButtonStyle.blurple, custom_id='0')]
    else:
      embed.title = '🔇Заткнули ебальники!'
      buttons = [Components.create_button(label='Пагаварить', style=ButtonStyle.blurple, custom_id='0')]
    actionrow = Components.create_actionrow(*buttons)
    await ctx.send(embed=embed, components=[actionrow])

    presssed = await Components.wait_for_component(self.bot, components=actionrow)
    await presssed.edit_origin()
    await self.amongus(ctx)'''

    @commands.Cog.listener('on_message')
    async def new_message(self, message):
        global msg_debt, meme_debt
        if message.channel.id == CHANNEL_MEMES and not message.author.bot and \
                (len(message.attachments) > 0 or 'https://' in message.content or 'http://' in message.content):
            await message.add_reaction('🤍')

    @commands.Cog.listener('on_message')
    async def direct_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel) and message.author.name != 'Гошик':
            author = message.author
            embed = discord.Embed(color=discord.Color.blue())
            if len(message.content) > 200:
                embed.title = f'📩 \"{message.content[:200]}...\"'
            else:
                embed.title = f'📩 \"{message.content}\"'
            embed.set_author(name=author.name, icon_url=author.avatar.url)
            embed.set_footer(text=str(message.author.id))
            channel = self.bot.get_channel(CHANNEL_GOSHIK)
            await channel.send(embed=embed)

    @commands.Cog.listener('on_member_join')
    async def member_enter(self, member):
        await member.send(answer_welcome)
        channel = self.bot.get_channel(CHANNEL_CHAT)
        embed = discord.Embed(color=0)
        embed.title = f'🥳 {member.name} подключается!'
        embed.description = 'Теперь на сервере на одного дебила больше!'
        await channel.send(embed=embed)

    @commands.Cog.listener('on_member_remove')
    async def member_exit(self, member):
        channel = self.bot.get_channel(CHANNEL_CHAT)
        embed = discord.Embed(color=0)
        embed.title = f'😪 {member.name} куда-то ушёл...'
        embed.description = 'Press F'
        message = await channel.send(embed=embed)
        await message.add_reaction('🇫')

    @discord.Cog.listener('on_command_error')
    async def error_handler(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        channel = self.bot.get_channel(CHANNEL_GOSHIK)
        await channel.send(error)
        raise error


def setup(bot):
    bot.add_cog(Admin(bot))
