# Pokemon Companion

The Pokemon Companion web app serves as a one stop shop to help you through your pokemon journey. It serves as a Pokedex to get information on specific pokemon as well as a battle helper to help you optimize your teams against tough opponents.

## Table of Contents

- [About](#about)  
- [Motivation & Goals](#motivation--goals)  
- [Key Features](#key-features)  
- [Screenshots](#demo--screenshots)  
- [Tech Stack & Dependencies](#tech-stack--dependencies)  
- [Installation & Setup](#installation--setup)  
- [Usage](#usage)  
- [Project Structure](#project-structure)
- [Project File Summaries](#project-file-structure)
- [PokeAPI Reference](#pokeapi-reference)
- [Design Choices](#design-decisions--trade-offs)  
- [Future Improvements](#future-improvements)

---

## About

Pokemon Companion is a full-stack web application that provides:

- A browsable Pokedex (all Pokemon, grouped by generation), with detailed pages (types, abilities, moves, evolutions).  
- A **Team Builder** for logged-in users to create and manage multiple teams (up to 6 Pokemon per team).  
- A **Battle Helper** that, given an opponent Pokemon, evaluates all your teams and suggests which of your Pokemon are best suited — based on type matchups.  

It’s designed to be intuitive, responsive, and helpful for beginners wanting to get into the world of Pokemon.

---

## Motivation & Goals

I built this project as my final project for Harvard’s CS50 — to apply what I learned about web development (Flask/SQLite/templating) and to build something **useful**, **interactive**, and **fun**.  

My goals were:  
- To explore using a public API to dynamically fetch and cache Pokemon data.  
- To design a clean, responsive UI that works well on desktop and mobile.  
- To build non-trivial features: persistent user accounts, dynamic team building, logic for type-matchup analysis.  
- To build a pokemon battle helper that takes into account opponent stats, types as well as move sets.

---

## Key Features

- **Pokedex Page** — Browse all Pokemon by generation, each card clickable to a detailed page.  
- **Pokemon Detail Page** — View sprite (regular + shiny), types, abilities, full move list (with power, accuracy, PP), and evolution chain.  
- **User Authentication** — Register / Login / Logout with secure password hashing and sessions.  
- **Team Builder** — Logged-in users can create multiple teams, add up to 6 Pokemon per team, name their teams, and edit or delete them.  
- **Battle Helper** — Given an opponent Pokemon, the app analyzes your teams and highlights which Pokemon are strong / neutral / weak against that opponent.  
- **Caching System** — Pokemon data is cached locally (JSON + SQLite) to avoid repeated API calls and improve performance.  
- **Responsive Design** — Uses Bootstrap to adapt to different screen sizes (mobile → desktop).  

---

## Demo / Screenshots

*If you have screenshots or a deployed version, add them here (GIFs or images help a lot).*



---

## Tech Stack & Dependencies

- **Backend**: Python 3.x, Flask  
- **Database**: SQLite (for user accounts, team storage, caching)  
- **Frontend**: HTML + Jinja2 templates, Bootstrap 5, custom CSS  
- **Dependencies** (in `requirements.txt`):  
  - Flask  
  - Werkzeug (for password hashing)  
  - requests (if you fetch from external API)  
  - sqlite3 (builtin)  
- **Data Source / API**: PokeAPI (data cached locally)  

---

## Installation & Setup

1. Clone the repository  
   ```bash
   git clone https://github.com/Hamza-Salman/Pokemon_Companion.git
   cd Pokemon_Companion
   ```

2. Create a virtual environment and activate it
    ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
   ```

4. Initialize database
    ```bash
    sqlite3 pokemonCompanion.db
   ```

5. Create database tables with the schema provided
    ```sql
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL
    );
    CREATE UNIQUE INDEX username ON users (username);

    CREATE TABLE user_teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        team_name TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    CREATE UNIQUE INDEX idx_teams_user_name ON user_teams (user_id, team_name);

    CREATE TABLE team (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER NOT NULL,
        pokemon_name TEXT NOT NULL,
        slot INTEGER NOT NULL CHECK (slot BETWEEN 1 AND 6),
        FOREIGN KEY(team_id) REFERENCES teams(id),
        UNIQUE(team_id, slot)
    );
   ```

6. Run the Flask server
    ```bash
    flask run
   ```

7. Visit the app in your browser: http://localhost:5000

## Usage

- **Anonymous users**: can browse the Pokedex, view Pokemon details.

- **Registered users**: can build teams, view them, and use the Battle Helper.

- On the Battle Helper page: select an opponent Pokemon → submit → see results with color-coded strength bars for each team’s Pokemon.

- Teams can be viewed or deleted as needed via the “My Teams” page.

## Project Structure
```
/Pokemon_Companion
│   app.py             # Flask application routes
│   helpers.py         # Database + API helper functions
│   requirements.txt
│   README.md          # ← this file
│
├── templates/         # html templates
│     layout.html
│     index.html
│     login.html
│     register.html
│     pokedex.html
│     pokemon.html
│     create_team.html
│     teams.html
│     battle-helper.html
│     battle-results.html
│     move_cache.json       # JSON cache files are created after first run
│     not_found_cache.json  
│     pokemon_cache.json    
│
└── static/            # static assets
      styles.css
```

## Project File Summaries

`app.py` is the core of the Pokemon Companion application and defines **all Flask routes**, session configuration, page rendering, user authentication, team management, and the battle helper logic. It acts as the main controller for the entire project.

`helpers.py` contains all utility functions used throughout the application, including database helpers, Pokemon data fetchers that interface with the API, caching logic, and type effectiveness tools. It serves as the backend “logic layer” supporting `app.py`.

**Templates**  
All the HTML files for the individual web pages:
- layout.html
- index.html
- login.html
- register.html
- pokedex.html
- pokemon.html
- create_team.html
- teams.html
- battle-helper.html
- battle-results.html

**JSON Files**  
Files used for caching data
- `pokemon_cache.json`: Used for storing all Pokemon data pulled from the API
- `move_cache.json`: Used for storing all move data pulled from the API. This is necessary as move data is pulled from a seperate API call than the Pokemon API call. Otherwise there can be up to 249 different API calls for a single Pokemon. (The Pokemon Mew can learn 249 unique moves)
- `not_found_cache.json`: Used for storing the names of pokemon that the API fails on. There are certain pokemon that the API fails to return data on. Might be because of server issues or missing data. However I have still included them in case that data gets fixed. There is a boolean constant in the `helpers.py` called `CHECK_NOT_FOUND` This can be changed to completely ignore the Pokemon that are not found by the API to improve performance of web pages. This is because if it was left as True, it would still make the api calls for all the Pokemon that are not found and slow down the loading of web pages.

## PokeAPI Reference 

For more information: [PokeAPI Documentation](https://pokeapi.co/)

### Get All Pokemon by Generation

```http
  https://pokeapi.co/api/v2/generation/{gen}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of generation |

Used to pull the name of all Pokemon by generation.

### Get Pokemon data by name

```http
  https://pokeapi.co/api/v2/pokemon/{pokemon_name}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Required**. Id of pokemon to fetch |

Used to get data specific to the individual pokemon. (example: id, sprite, types, abilities...)

### Get Pokemon Species Data and Evolution Chain Data

```http
  https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Required**. Name of pokemon to fetch |

Used to get the evolution chain id for a specific pokemon

```http
  https://pokeapi.co/api/v2/evolution-chain/{id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of evolution chain to fetch |

Used to get list of all pokemons in a specific pokemons evolution chain.

### Get Pokemon Move data

```http
  https://pokeapi.co/api/v2/move/{name}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Required**. Name of move to fetch |

Gets data specific to a move. (example: type, power, accuracy, pp)

### Get Pokemon Type data

```http
  https://pokeapi.co/api/v2/type/{name}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Required**. Name of type to fetch |

Used to get strengths and weaknesses of a specific pokemon type. Used for the battle helper

## Design Choices
| Decision                                                 | Reason / Trade-off                                                                                                                       |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Use SQLite + JSON cache                                  | Easy to set up; no external DB required. Might limit scalability for large user base.                                                    |
| Client-side search / select for Pokémon lists            | Fast UI, no extra server calls. May be slow for very large lists on old devices — could optimize later with paging or virtualized lists. |
| Simple strength classification (strong / neutral / weak) | Easy to implement and understand; not an exact calculation of all battle mechanics (stats, abilities, synergy).                          |
| Cacheing Pokemon data rather than pulling from API on each call         | Enables faster load times and prevents throttling from the PokeAPI servers.                                                                               |

## Future Improvements
- Add type-chart calculation (resistances, immunities, dual-type interactions) for more accurate battle advice.

- Add Pokemon movesets to battle helper calculations.

- Add ability to build team for opponent

- Improve performance for large number of Pokémon (e.g., lazy-load sprites, paginate lists).

- Add search / filter / sort for teams (by name, by strength against a certain type, etc.).