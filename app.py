from flask import Flask, redirect, render_template, request
import json

from helpers import fetch_pokemon_generation, fetch_pokemon_data

app = Flask(__name__)

NUM_GENS = 9

@app.route("/")
def index():
    #TODO: Homepage. Have info on project and features
    return render_template('/index.html')

@app.route("/pokedex", methods=["GET", "POST"])
def pokedex():
    #TODO: Have a list of all pokemon broken down by generations
    if request.method == "POST":
        gen = request.form.get("generation")
        pokemons = []
        if gen == "all":
            for i in range(1, NUM_GENS):
                pokemons += fetch_pokemon_generation(i)
        else:
            pokemons = fetch_pokemon_generation(gen)
        return render_template("/pokedex.html", pokemons=pokemons)
    else:
        pokemons = fetch_pokemon_generation(1)
        return render_template("/pokedex.html", pokemons=pokemons)

@app.route("/pokemon", methods=["GET", "POST"])
def pokemon():
    if request.method == "POST":
        pokemon_name = request.form.get("pokemon_name")
        pokemon_data = fetch_pokemon_data(pokemon_name)
        return render_template("/pokemon.html", pokemon_data=pokemon_data)
    #TODO: 
    return "Hello, World!"

@app.route("/register")
def register():
    #TODO: 
    return "Hello, World!"

@app.route("/login")
def login():
    #TODO: 
    return "Hello, World!"

@app.route("/logout")
def logout():
    #TODO: 
    return "Hello, World!"

@app.route("/team")
def team():
    #TODO: 
    return "Hello, World!"

@app.route("/battle-helper")
def battle():
    #TODO: 
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)