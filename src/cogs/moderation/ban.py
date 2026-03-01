import fluxer
import os
from dotenv import load_dotenv
from fluxer.models import Embed

# Global values gathered from .env, do not modify.
GUILD_ID = int(os.getenv("GUILD_ID"))
DEBUG = int(os.getenv("BOT_DEBUG_MODE"))
MOD_ROLE = int(os.getenv("MOD_ROLE"))

class BanCog(fluxer.Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @fluxer.Cog.command(name="ban")  
    async def ban(self, ctx, *, args: str):
        parts = args.split(" -r ")
        member_ids = [int(x.strip()) for x in parts[0].split()]
        reason = parts[1].strip() if len(parts) > 1 else "No reason provided"
        guild = await self.bot.fetch_guild(ctx.guild_id) 
        
        if not guild:  
            return ctx.reply("This command hasn't been run in a guild, how are you using this bot?")  
        
        # Permission gating, only mods can use this command.
        author_id = getattr(ctx.author, "user", ctx.author).id  

        member = await guild.fetch_member(author_id)  
        if not member or not member.has_role(MOD_ROLE):  
            await ctx.reply("Oops! You do not have permission to use that command.")  
            print("[WARNING] Someone without the mod role tried to use the ban command!")  
            return  
        
        banned_count = 0  
        failed_bans = []  
          
        for member_id in member_ids:  
            try:  
                await guild.ban(user_id=member_id, reason=reason)
                banned_count += 1
                if DEBUG == 1:  
                    print(f"[DEBUG] Ban command operated on {member_id}")
            except Exception as e:  
                failed_bans.append(f"{member_id} ({str(e)})")  
    
        # Create response embed  
        if banned_count > 0:  
            bannedEmbed = Embed(  
                title=f"Banned {banned_count} member{'s' if banned_count > 1 else ''}",  
                description=f"Banned IDs: {', '.join(map(str, member_ids))}\nReason: {reason}",  
                color=0x65b7e6  
            )  
            await ctx.reply(embed=bannedEmbed)

            if failed_bans:  
                await ctx.reply(f"Failed to ban: {', '.join(failed_bans)}")  

        
async def setup(bot):
    await bot.add_cog(BanCog(bot))