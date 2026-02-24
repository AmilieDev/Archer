import fluxer
import os
from dotenv import load_dotenv
from fluxer.models import Embed

# Global values gathered from .env, do not modify.
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
DEBUG = int(os.getenv("BOT_DEBUG_MODE", "0"))
MOD_ROLE = int(os.getenv("MOD_ROLE", "0"))

class KickCog(fluxer.Cog):
    def __init__(self, bot):
        super().__init__(bot)

    reason = "No reason set."

    @fluxer.Cog.command(name="kick")
    async def kick(self, ctx, member_id: int, *, reason: str | None = None):
        guild = await self.bot.fetch_guild(ctx.guild_id)  

        if not guild:
            return await ctx.reply("This command hasn't been run in a guild, how are you using this bot?")
        await guild.kick(user_id=member_id, reason=reason)

        # Permission gating, only mods can use this command.
        author_id = getattr(ctx.author, "user", ctx.author).id  

        member = await guild.fetch_member(author_id)  
        if not member or not member.has_role(MOD_ROLE):  
            await ctx.reply("Oops! You do not have permission to use that command.")  
            print("[WARNING] Someone without the mod role tried to use the kick command!")  
            return  

        kickedEmbed = Embed(
            title = f"Kicked {member_id}",
            description = f"This member hass been kicked for: {reason}",
            color=0x65b7e6
        )

        await ctx.reply(embed=kickedEmbed)  

        logger = self.bot.cogs.get("LoggerCog")
        if logger:
            await logger.send_signal(
                logger.SignalCategory.MODERATION,
                logger.ModerationSignal.BAN,
                moderator=ctx.author,
                target=member,
                reason=reason
            )

        if DEBUG == 1:
            print(f"[DEBUG] Kick command operated on {member_id}")
            
async def setup(bot):
    await bot.add_cog(KickCog(bot))