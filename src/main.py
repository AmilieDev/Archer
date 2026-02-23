# This code is licensed under the GPLv2, feel free to tweak, redistribute or do whatever you want really.
# See license.md for more information :)

from dotenv import load_dotenv
import fluxer
import os

# Initialise .env > You bot token should be in this virtual environment unless
# you're using docker-deploy. In which case paste the token in bot_token.txt!
if not os.getenv('DOCKER_DEPLOY'):
    load_dotenv()

INTENTS = os.getenv("FLUXER_INTENTS")
PREFIX = os.getenv("BOT_PREFIX")
DEBUG = int(os.getenv("BOT_DEBUG_MODE"))

bot = fluxer.Bot(command_prefix=PREFIX, intents=INTENTS)

@bot.event
async def on_ready():
    print(f"[OK] loading cogs, please wait...")
    await load_extensions()
    print(f"[OK] Bot has started and logged into Fluxer as with Fluxer as: {bot.user.username}")

async def load_extensions():
    for root, dirs, files in os.walk("./src/cogs"):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                path = os.path.join(root, filename)
                cog = path.lstrip("./").replace(os.sep, ".")[:-3]
                cog = cog.removeprefix("src.")
                try:
                    await bot.load_extension(cog)
                    if DEBUG == 1:
                        print(f"[DEBUG] Loaded {cog}")
                except Exception as e:
                    print(f"[ERROR] Failed to load {cog}: {e}")

if __name__ == "__main__":
    # !!! SECURITY WARNING!!!
    # NEVER, EVER, EVER UNDER ANY CIRCUMSTANCES PUT YOUR TOKEN HERE.
    # PUT YOUR TOKEN IN .ENV IN THE PROJECT ROOT.
    # THANK YOU.
    if not os.getenv('DOCKER_DEPLOY'):
        TOKEN = os.getenv('FLUXER_BOT_TOKEN')
    else:
        with open("/run/secrets/FLUXER_BOT_TOKEN") as f:
            TOKEN = f.read().strip()

    bot.run(TOKEN)
