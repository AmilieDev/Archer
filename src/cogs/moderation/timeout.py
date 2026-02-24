import fluxer
import os
from dotenv import load_dotenv
from fluxer.models import Embed
from datetime import datetime, timedelta  

# Global values gathered from .env, do not modify.
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
DEBUG = int(os.getenv("BOT_DEBUG_MODE", "0"))
MOD_ROLE = int(os.getenv("MOD_ROLE", "0"))

# TIme parsing, for date & time in timeout, max 14d.
def parse_duration(duration: str) -> datetime:  
    unit = duration[-1].lower()  
    value = int(duration[:-1])  
    if unit == "d":  
        delta = timedelta(days=value)  
    elif unit == "h":  
        delta = timedelta(hours=value)  
    elif unit == "m":  
        delta = timedelta(minutes=value)  
    else:  
        raise ValueError("Use d/h/m suffix (e.g., 14d, 1h, 30m).")  
    if delta > timedelta(days=14):  
        raise ValueError("Timeout cannot exceed 14 days.")  
    return datetime.utcnow() + delta

class TimeoutCog(fluxer.Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @fluxer.Cog.command(name="timeout")
    async def timeout(self, ctx, member_id: int, *, reason: str, time: str):
        guild = await self.bot.fetch_guild(ctx.guild_id)  

        if not guild:
            return await ctx.reply("This command hasn't been run in a guild, how are you using this bot?")
        
        # Permission gating, only mods can use this command.
        author_id = getattr(ctx.author, "user", ctx.author).id  
        guild = await self.bot.fetch_guild(ctx.guild_id)  

        member = await guild.fetch_member(author_id)  
        if not member or not member.has_role(MOD_ROLE):  
            await ctx.reply("Oops! You do not have permission to use that command.")  
            print("[WARNING] Someone without the mod role tried to use the timeout command!")  
            return  
        
        member = await guild.fetch_member(member_id)  
        until_iso = parse_duration(time).isoformat() + "Z"  
        await member.timeout(until=until_iso, reason=reason, guild_id=guild.id)

        timedoutEmbed = Embed(
            title = f"Timed Out {member_id}",
            description = f"This member hass been timed out for: {reason}, for {time}",
            color=0x65b7e6
        )

        await ctx.reply(embed=timedoutEmbed)

        if DEBUG == 1:
            print(f"[DEBUG] Kick command operated on {member_id}")
        
async def setup(bot):
    await bot.add_cog(TimeoutCog(bot))