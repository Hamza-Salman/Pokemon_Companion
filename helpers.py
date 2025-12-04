import requests
import json
import os
from flask import redirect, render_template
from functools import wraps

CACHE_FILE = "pokemon_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# ================= This method fetches the data for the generations for the pokedex page and caches it (USES /generation api call) =================
def fetch_pokemon_generation(gen):
    url = f"https://pokeapi.co/api/v2/generation/{gen}/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemons = []
        for pokemon in data['pokemon_species']:
            pokemon_data = fetch_pokemon_data(pokemon['name'])
            if pokemon_data:
                pokemons.append({"name" : pokemon['name'], "id": pokemon_data['id'], "sprite": pokemon_data['sprite']})
        pokemons.sort(key=lambda x: x['id'])
        return pokemons
    except requests.exceptions.RequestException as e:
        print(f"Error fetching generation {gen}: {e}")

# ================= This method fetches the data for the individual pokemon (USES /pokemon api call) =================
def fetch_pokemon_data(pokemon_name):

    pokemon_cache = load_cache()

    if pokemon_name in pokemon_cache:
        return pokemon_cache[pokemon_name]

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"

    try:
        print(f"Fetching data for {pokemon_name} from API.")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemon_info = {
            "name": data['name'],
            "id": data['id'],
            "sprite": data['sprites']['front_default'],
            "shiny": data['sprites']['front_shiny'],
            "types": [t['type']['name'] for t in data['types']],
            "abilities": [a['ability']['name'] for a in data['abilities']],
            "moves": [m['move']['name'] for m in data['moves']]
        }

        pokemon_cache[pokemon_name] = pokemon_info
        save_cache(pokemon_cache)

        return pokemon_info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {pokemon_name}: {e}")
        return None
    
# ================= This method fetches the data for the individual pokemons evolution chain (USES /pokemon-species api call) =================
# ================= This method also fetches the data for the individual pokemons evolutions using evolution chain (USES /evolution-chain api call) =================
def fetch_evoltion_chain(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        #chain url from species api call
        evolution_chain_url = data['evolution_chain']['url']

        #chain data from evolution chain api call
        response = requests.get(evolution_chain_url)
        response.raise_for_status()
        evo_data = response.json()

        chain = []
        branches = []
        current = evo_data['chain']

        while current:
            species_name = current['species']['name']
            chain.append(species_name)
            # Gets all the branches for pokemons that have multiple evolution variations
            if (len(current['evolves_to']) > 1):
                print("Branched evolution detected.")
                for branch in current['evolves_to']:
                    branches.append(branch['species']['name'])
                    print(f"Branch: {branch['species']['name']}")
                current = current['evolves_to'][0]
            elif current['evolves_to']:
                current = current['evolves_to'][0]
            else:
                current = None
        
        #added branched evolutions to chain
        for branch in branches:
            if branch not in chain:
                chain.append(branch)

        return chain
    except requests.exceptions.RequestException as e:
        print(f"Error fetching evolution chain for {pokemon_name}: {e}")
        return []