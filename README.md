# Pokémon Discord Bot — Übersicht & Leitfaden

  

Ein immersiver Discord-Bot, der das Spielgefühl der **Gameboy-Editionen (Gen 1 & 2)** nachbildet: 

Spieler fangen Pokémon, kämpfen, fordern Arenen heraus, sammeln Items und können AFK-Expeditionen starten.


---

  

##  Ziel & Spielerlebnis

- **Authentisches Gameplay**: Rundenbasierte Kämpfe, Typen-Logik, Status-Effekte, Fangmechanik.

- **Community-Fokus**: Öffentliche Spawns, private Kampf-Sessions, Live-Mitverfolgung.

##  Roadmap

1. **Bot-Setup & Datenmodell**
2. **Kampf-Engine (PvE/PvP) — Basisformel, Typen, Status**
3. **Spawning + Fangen** (Embed + „⚔️ Kämpfen“)
4. **Inventar + Pokécenter + Shop**
5. **Arena-System** (NPCs, Leiter, Orden)
6. **AFK-Exploration** (Gebiete, Berichte, Freischaltungen)
7. **Community-Features** (Live-Feed, Status-Board)
8. **Optimierung & Deployment** (SQLite, Caching, Logging)


##  Design-Prinzipien

- **Modularität**: saubere Trennung der Domänen.
- **Session-Management**: konfliktfreie parallele Kämpfe.
- **UI-Feedback**: Embed-Updates, nicht Chat-Spam.
- **Immersion**: Story-Text, visuelle Dynamik, kleine Animationen.
- **Fairness**: öffentliche Spawns + private Sessions, balancierte Chancen.
- **Individualisierung**: zufällige IVs, Geschlecht, Level pro Fang.