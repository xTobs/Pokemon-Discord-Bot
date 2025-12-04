import discord
from discord.ext import commands

TOKEN = "MTQ0NTg0NzQ2ODE3NTUyODEwMQ.GbAZU2.4USemlSJJ8OvlItk-BPdso6SBfMOnlfzb82G0E"
GUILD_ID = 474644609109065748  # Deine Server-ID
VOICE_CHANNEL_ID = 1445876406658662483  # ID des Voice-Channels

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        await channel.connect()
        print(f"Bot ist dem Voice-Channel '{channel.name}' beigetreten.")

bot.run(TOKEN)
