import fluxer
import os
from dotenv import load_dotenv
import asyncio

# Global values gathered from .env, do not modify.
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  

class RoleallCog(fluxer.Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @fluxer.Cog.command(name="roleall")
    async def roleall(self, ctx, role_id: int):
        author_id = getattr(ctx.author, 'user', ctx.author).id  

        if author_id != ADMIN_ID:
            await ctx.reply("Oops! You do not have permission to use that command.")
            print("[WARNING] Someone tried to role all!")
            return
        
        guild = self.bot._guilds.get(GUILD_ID)

        await ctx.reply("Assigning role to all users {role_id}")

        count = 0
        after = None
        while True:
            members = await guild.fetch_members(limit=100, after=after)
            if not members:
                break

            for member in members:
                try:
                    if role_id in [r.id for r in member.roles]:
                        continue

                    await member.add_role(role_id=role_id, guild_id=GUILD_ID, reason="Roleall Command")
                    count += 1

                    # This should shut up ratelimits.
                    await asyncio.sleep(0.6)

                except Exception as e:
                    print(f"[FAIL] Failed to add role to {member.user.id}")

                after = members[-1].user.id if members else None

        await ctx.reply(f"Added {role_id} to {count} members!")

async def setup(bot):
    await bot.add_cog(RoleallCog(bot))