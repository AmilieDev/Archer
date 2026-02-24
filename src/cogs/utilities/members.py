import fluxer
import os
from dotenv import load_dotenv

# Global values gathered from .env, do not modify.
GUILD_ID = int(os.getenv("GUILD_ID", "0"))

class MembersCog(fluxer.Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @fluxer.Cog.command(name="members")
    async def members(self, ctx):
        guild = self.bot._guilds.get(GUILD_ID)

        count = 0  
        after = None  
        while True:  
            members = await guild.fetch_members(limit=100, after=after)  
            if not members:  
                break  
            count += len(members)  
            after = members[-1].user.id  
  
        await ctx.reply(f"This guild currently has: {count} members!")  
        
async def setup(bot):
    await bot.add_cog(MembersCog(bot))