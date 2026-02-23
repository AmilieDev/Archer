# Archer

Archer is a free, open-source, and self-hostable utility bot for [Fluxer](https://fluxer.gg). It's built to be minimal and effective — no bloat, just the tools you need.

> Have questions or feedback? DM me on Fluxer: [arch](https://fluxer.gg/arch)

---

## Features

- **Moderation utilities** — keep your server in order
- **Role utilities** — includes `roleall` and autorole on member join
- **Coming soon** — Reaction Roles and more

---

## Getting Started

Archer currently supports **Unix-based systems** (macOS, Linux, FreeBSD). Make sure you have the required dependencies installed before proceeding.

First, install docker and docker-compose with your package manager of choice, eg.:
```pacman -S docker docker-compose```

Then, you'll want to edit the ```docker-compose.yml``` file to set all of the enviroment variables needed to run the bot **except the bot token**. The bot token for safety reasons is stored using a docker secret, which pulls the token from ```bot_token.txt```. Make sure to copy the bot token there. <br>
If you'd rather have the bot pull everything from the .env.example file, you can set the ```DOCKER_DEPLOY``` variable to False. However this is **not** recommened for docker compose deployments. <br>
(If you do end up doing it, make sure to remove the .example from the env file!)

And finally, to start your bot use
```sudo docker-compose up --build```<br>
If you do not want to use sudo you can also add your user to the docker group and run
```docker-compose up --build``` <br>
You can also run the container detached from your shell by running <br>
```docker-compose up -d --build```

Any changes will require you to use the above rebuild command, if you haven't made a change, but want to start your bot again - simply omit the --build part of the command.

Enjoy!

---

## Gateway Intents

When connecting to the Fluxer API/Gateway, you'll need to specify your intents as a bitfield. Set this value in your `.env` file.

To calculate your intent value, add up the values for each intent you want to enable.

| Intent | Bit | Value |
|--------|-----|-------|
| GUILDS | 1 << 0 | 1 |
| GUILD_MEMBERS | 1 << 1 | 2 |
| GUILD_MODERATION | 1 << 2 | 4 |
| GUILD_EMOJIS_AND_STICKERS | 1 << 3 | 8 |
| GUILD_INTEGRATIONS | 1 << 4 | 16 |
| GUILD_WEBHOOKS | 1 << 5 | 32 |
| GUILD_INVITES | 1 << 6 | 64 |
| GUILD_VOICE_STATES | 1 << 7 | 128 |
| GUILD_PRESENCES | 1 << 8 | 256 |
| GUILD_MESSAGES | 1 << 9 | 512 |
| GUILD_MESSAGE_REACTIONS | 1 << 10 | 1024 |
| GUILD_MESSAGE_TYPING | 1 << 11 | 2048 |
| DIRECT_MESSAGES | 1 << 12 | 4096 |
| DIRECT_MESSAGE_REACTIONS | 1 << 13 | 8192 |
| DIRECT_MESSAGE_TYPING | 1 << 14 | 16384 |
| MESSAGE_CONTENT | 1 << 15 | 32768 |

---

## Log Symbols

Archer uses the following prefixes in its console output:

| Symbol | Meaning |
|--------|---------|
| `[DEBUG]` | Verbose debug output (can be enabled in `.env`) |
| `[OK]` | Operation completed successfully |
| `[FAIL]` | Non-fatal error — the bot will continue running |
| `[ERROR]` | Fatal error — the bot will shut down to prevent further issues |

---

## License

This project is open-source. See [LICENSE](./LICENSE) for details.
