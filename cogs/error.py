import os
import traceback
import uuid
from datetime import datetime

import discord
from discord.ext import commands

from utils import is_mobile


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "⚠️ 명령에 누락된 항목이 있습니다. `?도움말` 명령어를 통해 정확한 사용법을 보실 수 있습니다.",
                delete_after=5,
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "⚠️ 잘못된 명령입니다. `?도움말` 명령어를 통해 정확한 사용법을 보실 수 있습니다.",
                delete_after=5,
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.send("⚠️ 관리자만 사용가능한 명령어입니다.", delete_after=5)
        else:
            trace_uuid = str(uuid.uuid4())
            await ctx.send(
                embed=discord.Embed(
                    title="⚠️ 알 수 없는 오류가 발생했습니다.",
                    description=f"다음 정보를 개발자에게 알려주시면 문제해결에 도움이됩니다.\n**UUID**: ``{trace_uuid}``\n\n베타테스트 기간입니다, 발생 경위를 <#751768265088565279>에 보내주세요.",
                    colour=discord.Color.red(),
                ),
                mobile=is_mobile(ctx.author),
            )

            trace_embed = discord.Embed(
                title=f"Unexpected Error in schoolbot\n**UUID**: ``{trace_uuid}``",
                description=f"**Version**: ``{self.bot.__version__}``\n"
                f"**User**: ``{ctx.author}`` (``{ctx.author.id}``)\n"
                f"**Guild**: ``{ctx.author.guild}`` (``{ctx.author.guild.id}``)\n"
                f"**Channel**: ``{ctx.channel}`` (``{ctx.channel.id}``)\n"
                f"**Command**: ``{ctx.command}``\n"
                f"**Bot Permission**: ``{ctx.guild.me.guild_permissions.value}``",
                timestamp=datetime.utcnow(),
            )
            if not error.__cause__:
                trace_embed.add_field(
                    name="Traceback:",
                    value=f"```py\n{''.join(traceback.format_exception(type(error), error, error.__traceback__, limit=3))}\n```",
                )
            else:
                trace_embed.add_field(
                    name="Traceback:",
                    value=f"```py\n{''.join(traceback.format_exception(type(error.__cause__), error.__cause__, error.__cause__.__traceback__, limit=3))}\n```",
                )

            channel = await self.bot.fetch_channel(os.environ["channel_id"])
            await channel.send(embed=trace_embed, mobile=is_mobile(ctx.author))


def setup(bot):
    bot.add_cog(Error(bot))
