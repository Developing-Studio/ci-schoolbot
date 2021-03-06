import discord
from discord.ext import commands


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Login.. : ")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("======================")
        print(f"{len(set(self.bot.get_all_members()))}명이 봇을 사용하고 있습니다..")
        print("======================")

        game = discord.Game(f"?도움말 | {self.bot.__version__}")
        await self.bot.change_presence(status=discord.Status.online, activity=game)


def setup(bot):
    bot.add_cog(Ready(bot))
