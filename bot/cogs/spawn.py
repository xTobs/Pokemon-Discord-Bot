
import asyncio
import random
import discord
from discord.ext import commands
from infra.config import load_config
from utils.pokemon_pool import random_species

cfg = load_config()

def _utcnow():
    # discord.py bietet utils.utcnow(); wir bleiben kompatibel
    try:
        from discord.utils import utcnow
        return utcnow()
    except Exception:
        import datetime as dt
        return dt.datetime.utcnow()

class CatchView(discord.ui.View):
    """MVP-View: Klick = Sofort-Fang. Timeout deaktiviert Buttons und aktualisiert die Nachricht."""
    def __init__(self, species_de: str, author_id: int | None = None, timeout: float | None = 120):
        super().__init__(timeout=timeout)
        self.species_de = species_de
        self.author_id = author_id
        self.caught_users: set[int] = set()
        self.message: discord.Message | None = None  # wird nach dem Senden gesetzt

    @discord.ui.button(label="⚔️ Kämpfen / Fangen", style=discord.ButtonStyle.success)
    async def catch_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Optional: Nur einmal pro User erlauben
        if interaction.user.id in self.caught_users:
            await interaction.response.send_message(
                f"Du hast **{self.species_de}** bereits gefangen! 🎒",
                ephemeral=True
            )
            return

        # Sofort-Fang (MVP)
        self.caught_users.add(interaction.user.id)
        await interaction.response.send_message(
            f"🎉 **Fang erfolgreich!** **{self.species_de}** wurde deinem Team hinzugefügt.",
            ephemeral=True
        )

    async def on_timeout(self) -> None:
        # Buttons deaktivieren und Nachricht aktualisieren
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        try:
            if self.message:
                await self.message.edit(view=self)
        except Exception:
            pass

class SpawnCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._runner_task: asyncio.Task | None = None

    def cog_unload(self):
        if self._runner_task and not self._runner_task.done():
            self._runner_task.cancel()

    def _next_delay(self) -> int:
        lo = min(cfg["SPAWN_MIN_SEC"], cfg["SPAWN_MAX_SEC"])
        hi = max(cfg["SPAWN_MIN_SEC"], cfg["SPAWN_MAX_SEC"])
        return random.randint(lo, hi)

    async def _join_voice_briefly(self):
        """Bot joint kurz den Voice-Channel. Keine Audioausgabe."""
        channel_id = cfg["VOICE_CHANNEL_ID"]
        if not channel_id:
            return
        channel = self.bot.get_channel(channel_id)
        if not isinstance(channel, discord.VoiceChannel):
            if cfg["DEBUG"]:
                print("[spawn] VOICE_CHANNEL_ID ist kein Sprachkanal.")
            return

        try:
            # Bereits verbunden?
            if channel.guild.voice_client and channel.guild.voice_client.is_connected():
                return

            # Versuch, zu verbinden
            vc = await channel.connect(self_deaf=True)
            await asyncio.sleep(3)  # kurzer „Ping“
            await vc.disconnect(force=True)
        except discord.Forbidden:
            if cfg["DEBUG"]:
                print("[spawn] Keine Berechtigung, Sprachkanal zu betreten.")
        except Exception as e:
            if cfg["DEBUG"]:
                print(f"[spawn] Voice-Join fehlgeschlagen: {e}")

    async def _spawn_once(self):
        """Eine Spawn-Runde: Pokemon wählen, Voice-Ping, Embed mit Button posten."""
        species = random_species(k=1)[0]

        # Voice-Aktion parallel starten
        voice_task = asyncio.create_task(self._join_voice_briefly())

        # Text-Spawn
        text_channel = self.bot.get_channel(cfg["TEXT_CHANNEL_ID"])
        if not isinstance(text_channel, (discord.TextChannel, discord.Thread)):
            if cfg["DEBUG"]:
                print("[spawn] TEXT_CHANNEL_ID ist kein Textkanal/Thread.")
            await voice_task
            return

        embed = discord.Embed(
            title="Du betrittst hohes Gras…",
            description=f"Ein wildes **{species}** erscheint!",
            color=discord.Color.brand_green(),
            timestamp=_utcnow(),
        )
        embed.set_footer(text="Klicke auf „⚔️ Kämpfen / Fangen“, um es sofort zu fangen (MVP).")

        view = CatchView(species_de=species, timeout=120)
        msg = await text_channel.send(embed=embed, view=view)
        view.message = msg

        await voice_task

    async def _runner(self):
        await self.bot.wait_until_ready()
        if cfg["DEBUG"]:
            print("[spawn] Runner gestartet.")
        try:
            while not self.bot.is_closed():
                # variabler Sleep
                delay = self._next_delay()
                if cfg["DEBUG"]:
                    print(f"[spawn] Nächster Spawn in {delay}s.")
                await asyncio.sleep(delay)
                await self._spawn_once()
        except asyncio.CancelledError:
            if cfg["DEBUG"]:
                print("[spawn] Runner beendet (cancelled).")
        except Exception as e:
            if cfg["DEBUG"]:
                print(f"[spawn] Runner-Fehler: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        # Runner beim ersten Ready starten (idempotent)
        if not self._runner_task or self._runner_task.done():
            self            self._runner_task = asyncio.create_task(self._runner())

async def setup(bot: commands.Bot):