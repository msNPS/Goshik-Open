import discord
from discord.ext import commands
from config import *


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_raw_reaction_add')
    async def role_reaction_add(self, reaction):
        if reaction.message_id == MESSAGE_ROLES:
            guild = self.bot.get_guild(SERVER_ID)
            emoji = reaction.emoji.name
            role = guild.get_role(int(REACT_ROLES[emoji]))
            member = guild.get_member(reaction.user_id)
            await member.add_roles(role)

    @commands.Cog.listener('on_raw_reaction_remove')
    async def role_reaction_remove(self, reaction):
        if reaction.message_id == MESSAGE_ROLES:
            guild = self.bot.get_guild(SERVER_ID)
            emoji = reaction.emoji.name
            role = guild.get_role(int(REACT_ROLES[emoji]))
            member = guild.get_member(reaction.user_id)
            await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))
