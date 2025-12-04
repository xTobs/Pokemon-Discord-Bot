
import random

# MVP: Route-1-artige Pokémon (DE-Namen, Gen1-Feeling)
POKEMON_POOL = [
    "Taubsi",    # Pidgey
    "Rattfratz", # Rattata
    "Raupy",     # Caterpie
    "Hornliu",   # Weedle
    "Pikachu",   # Pikachu (selten)
]

WEIGHTS = [40, 40, 10, 8, 2]  # simple Gewichte

def random_species() -> str:
    return random.choices(POKEMON_POOL, weights=WEIGHTS, k=1)[0]
