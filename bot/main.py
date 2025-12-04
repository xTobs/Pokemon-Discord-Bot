
import asyncio
import discord
from discord.ext import commands
from infra.config import load_config

cfg = load_config()

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True  # optional; für klassische Nachrichten/Debug

async def main():
    if not cfg["DISCORD_TOKEN"]:
        raise RuntimeError("Bitte DISCORD_TOKEN in .env setzen.")

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Eingeloggt als {bot.user} (ID: {bot.user.id})")

    # Cogs laden
    await bot.load_extension("bot.cogs.spawn")

    try:
        await bot.start(cfg["DISCORD_TOKEN"])
    finally:
        #        # Sicherer Shutdown
        await bot.close()

if __name__ == "__main__":