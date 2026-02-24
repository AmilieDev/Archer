import fluxer
import os
from pathlib import Path
import shutil
from fluxer.models import Embed
import asyncio

REPO_URL= os.getenv("REPO_URL")
TEMP_DIR= Path("/tmp/archer")
LOCAL_COGS_DIR = Path("./src/cogs")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  

class UpdateCog(fluxer.Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @fluxer.Cog.command()
    async def update(self, ctx):
        author_id = getattr(ctx.author, 'user', ctx.author).id  

        if author_id != ADMIN_ID:
            await ctx.reply("Oops! You do not have permission to use that command.")
            print("[WARNING] Someone tried to update the bot!")
            return
        

        # Fancy! Embeds, makes it look all good.
        startingUpdateEmbed = Embed(
            title = "Starting update",
            description = "Hold tight! Updating now...",
            color=0x65b7e6
        )

        updateSuccessEmbed = Embed(
            title = "Sucessful update!",
            description = "Your bot should be ready to go with all the newst features!",
            color=0x65b7e6
        )

        updateFailedEmbed = Embed(
            title = "Uh oh! Update failed :(",
            description = "Something went wrong! Please check the logs!",
            color=0x991423
        )
        await ctx.reply(embed=startingUpdateEmbed)

        try:
            # Cloning and/or pulling the repository based on if it exists or not.
            if TEMP_DIR.exists():
                proc = await asyncio.create_subprocess_exec("git", "pull", cwd=TEMP_DIR, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            else:
                proc = await asyncio.create_subprocess_exec("git", "clone", REPO_URL, str(TEMP_DIR), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            # Catch if update failed (so any code other than 0)
            if proc.returncode != 0:
                await ctx.reply (embed=updateFailedEmbed)
                return
            
            # If update did work, and continues, then copy over the cogs.
            remote_cogs = TEMP_DIR / "src" / "cogs"
            if not remote_cogs.is_dir():
                await ctx.reply(embed=updateFailedEmbed)
                print("[ERROR] Couldn't update! There's no cogs directory in the Git library, are you using the correct repo format?")
                return
            
            # Copy cogs, mkdir if needed.
            copied = 0
            for entry in remote_cogs.rglob("*.py"):
                if entry.name.startswith("_"):
                    continue
                rel = entry.relative_to(remote_cogs)
                dest = LOCAL_COGS_DIR / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(entry, dest)
                copied += 1

            # Reloading cogs, for post update.
            print("[OK] Updated successfully copied cogs. Beginning reload.")
            for root, dirs, files in os.walk("./src/cogs"):
                for filename in files:
                    if filename.endswith(".py") and not filename.startswith("_"):
                        path = os.path.join(root, filename)
                        cog = path.lstrip("./").replace(os.sep, ".")[:-3]
                        cog = cog.removeprefix("src.")

                        # Actually begin reloading the cog.
                        try:
                            if cog in self.bot.extensions:
                                await self.bot.reload_extension(cog)
                                print(f"[OK] Reloaded {cog}")
                            else:
                                await self.bot.load_extension(cog)
                                print(f"[OK] Loaded {cog}")
                        except Exception as e:
                            print(f"[ERROR] Failed to reload {cog}: {e}")
                                
        except Exception as e:  
            print(f"[ERROR] Failed to update, please see logs.")

        await ctx.reply(embed=updateSuccessEmbed)

async def setup(bot):
    await bot.add_cog(UpdateCog(bot))