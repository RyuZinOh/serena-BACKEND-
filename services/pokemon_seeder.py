import random
import requests

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
    random_id = random.randint(1, 898)
    print(f"Generated random ID: {random_id}") 

    url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        types = [t['type']['name'].capitalize() for t in data['types']]
        iv = generate_random_iv()
        sprite = data['sprites']['front_default']
        
        pokemon = {
            "name": name,
            "types": types,
            "sprite": sprite,
            "iv": iv
        }

        return {"message": "Random Pokemon spawned successfully!", "pokemon": pokemon}, 200
    else:
        return {"error": "Failed to fetch data from PokeAPI."}, 500
