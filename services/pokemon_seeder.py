import random

pokemon_names = ["Pikachu", "Bulbasaur", "Charmander", "Squirtle", "Eevee", "Snorlax", "Jigglypuff", "Meowth", "Pidgey", "Magikarp"]

pokemon_types = ["Fire", "Water", "Grass", "Electric", "Psychic", "Normal", "Fairy", "Fighting", "Dark", "Ghost"]

def generate_random_iv():
    return {
        "hp": random.randint(0, 31),
        "attack": random.randint(0, 31),
        "defense": random.randint(0, 31),
        "special_attack": random.randint(0, 31),
        "special_defense": random.randint(0, 31),
        "speed": random.randint(0, 31)
    }

def spawn_random_pokemon():
    name = random.choice(pokemon_names)
    
    types = random.sample(pokemon_types, k=random.randint(1, 2))
    
    iv = generate_random_iv()

    sprite = f"https://img.pokemondb.net/sprites/diamond-pearl/normal/{name.lower()}.png"

    pokemon = {
        "name": name,
        "types": types,
        "sprite": sprite,
        "iv": iv
    }

    return {"message": "Random Pokemon spawned successfully!", "pokemon": pokemon}, 200
