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
            "shiny": data['sprites']['front_shiny']
        }

        pokemon_cache[pokemon_name] = pokemon_info
        save_cache(pokemon_cache)

        return pokemon_info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {pokemon_name}: {e}")
        return None