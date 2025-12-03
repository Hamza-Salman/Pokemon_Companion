import requests

from flask import redirect, render_template
from functools import wraps


def fetch_pokemon_generation(gen):
    url = f"https://pokeapi.co/api/v2/generation/{gen}/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemons = []
        for pokemon in data['pokemon_species']:
            pokemon_data = fetch_pokemon_data(pokemon['name'])
            pokemons.append({"name" : pokemon['name'], "id": pokemon_data['id'], "sprite": pokemon_data['sprite']})
        pokemons.sort(key=lambda x: x['id'])
        return pokemons
    except requests.exceptions.RequestException as e:
        print(f"Error fetching generation {gen}: {e}")

def fetch_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemon_info = {
            "name": data['name'],
            "id": data['id'],
            "sprite": data['sprites']['front_default'],
        }
        return pokemon_info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {pokemon_name}: {e}")
        return None