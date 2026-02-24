import fluxer
import os
from enum import Enum

LOGS_CHANNEL = os.getenv("LOGS_CHANNEL", "0")

class LoggerCog(fluxer.Cog):
    def __init__(self, bot):
        super().__init__(bot)

    class SignalCategory(Enum):
        MODERATION = "moderation"
        UTILITY = "utility"
        DEV = "dev"

    class ModerationSignal(Enum):
        BAN = "ban"
        KICK = "kick"
        TIMEOUT = "timeout"
        PURGE = "purge"

    class UtilitySignal(Enum):
        ROLEALL = "roleall"
        AUTOROLE = "autorole"
        MEMBERS = "members"

    class DevSignal(Enum):
        UPDATE = "update"
        RELOAD = "reload"
        PING = "ping"

    async def send_signal(self, category: "LoggerCog.SignalCategory", signal: Enum, **data):
        channel = await self.bot.fetch_channel(int(LOGS_CHANNEL))
        if channel is None:
            return

        logger_embed = fluxer.Embed(
            title=f"{category.value.upper()} | {signal.value.upper()}",
            description="\n".join(f"**{k}**: {v}" for k, v in data.items()),
            color=0x2F3136
        )
        await channel.send(embed=logger_embed)

    @fluxer.Cog.command()
    async def update(self, ctx):
        await self.send_signal(
            LoggerCog.SignalCategory.DEV,
            LoggerCog.DevSignal.UPDATE,
            invoker=ctx.author,
            guild=ctx.guild.name
        )

async def setup(bot):
    await bot.add_cog(LoggerCog(bot))