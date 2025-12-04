from flask import Flask, redirect, render_template, request, session
from helpers import fetch_pokemon_generation, fetch_pokemon_data, fetch_evoltion_chain, query_db
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


NUM_GENS = 9

@app.route("/")
def index():
    #TODO: Homepage. Have info on project and features
    database_test = query_db("SELECT * FROM users;")
    print(database_test)
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

        # gets evolutions
        evolutions = []
        evolution_chain = fetch_evoltion_chain(pokemon_name)
        for pokemon in evolution_chain:
            evolution_data = fetch_pokemon_data(pokemon)
            if evolution_data:
                evolutions.append(evolution_data)


        return render_template("/pokemon.html", pokemon=pokemon_data, evolutions=evolutions)
    #TODO: 
    return "Hello, World!"

@app.route("/register", methods=["GET", "POST"])
def register():
    #TODO: 
    if request.method == "POST":
        # Check if all values exist
        username = request.form.get("username")
        if not username:
            return render_template("/error.html", error="Missing Username")

        password = request.form.get("password")
        if not password:
            return render_template("/error.html", error="Missing Password")

        password_check = request.form.get("confirmation")
        if password != password_check:
            return render_template("/error.html", error="Passwords Don't Match")

        # Check if username is already taken
        if len(query_db("SELECT * FROM users WHERE username = ?",(username,))) != 0:
            return render_template("/error.html", error="username taken")

        # else add user to database
        else:
            # using try catch to add user in case there is any issues on the database side.
            try:
                query_db("INSERT INTO users (username, hash) VALUES (?, ?)", (username, generate_password_hash(password)), commit=True)
            except Exception as e:
                return render_template("/error.html", error="Error while adding User")

        # query database to make sure user is added
        rows = query_db("SELECT * FROM users WHERE username = ?", (username,))
        print("====================")
        print(rows)
        print("====================")
        # log user into current session
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/")
    else:
        return render_template("/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    #TODO: 

    if request.method == "POST":

        session.clear()

        if not request.form.get("username"):
            return render_template("/error.html", error="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("/error.html", error="must provide password")

        # Query database for username
        rows = query_db("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("/error.html", error="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("/login.html")

@app.route("/logout")
def logout():
    #TODO: 

    session.clear()

    return redirect("/")

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