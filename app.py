from flask import Flask, redirect, render_template

from helpers import fetch_pokemon_generation

app = Flask(__name__)

@app.route("/")
def index():
    #TODO: Homepage. Have info on project and features
    return render_template('/index.html')

@app.route("/pokedex")
def pokedex():
    #TODO: Have a list of all pokemon broken down by generations
    pokemons = fetch_pokemon_generation(1)
    return render_template("/pokedex.html", pokemons=pokemons)

@app.route("/pokemon")
def pokemon():
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