# Mobile Gacha API

## Full Stack Capstone Project

With the success of mobile gacha games in the last decade, players look to online databases to help them navigate the vast number of cards available to them. This application is built to create an API that is simple but also easily extensible so that it may be used as as a starting point for many different games

In this application, we will follow a common structure used in many games. This structure includes the following models:

- Characters - A cast of reoccurring characters that the game features in the main card system.
- Cards - A pool of cards available to 'pull' from via gacha mechanics. Each card features a character and has its own unique attributes.
- Skills - Various skills attached to different cards that serve to add depth to gameplay by allowing players to score better in-game.

This common structure is found in many mobile gacha games and can be very much likened to trading card games in a digital format. If you are familiar with either mobile gacha games or trading cards it's easy to see how these games are variants of the same format. Be it different naming conventions or extending typing or classes, if you take notice of these games' patterns you should have no problem modifying the database models to meet the needs of any number of games.

The application is set up with a Flask server with a SQLAlchemy module to handle our postgreSQL database. With Flask-Migrate for database migrations, we simplify the process of handling changes to our schema. Lastly, we use the third-party authentication service Auth0 to enable the application's role-based access control (RBAC) to manage member and contributor roles.

## Setting up the Application

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

It's recommended that you work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the postgres database.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Database Setup

Set the database path in the file `./database/database.py` to the postgres database you would like to use for this application.

```py
database_path = "postgres://{}/{}".format('localhost:5432', database_name)
```

To restore the database with the example capstone_db.psql file provided run:

```bash
psql database_name < database/gacha.psql
```

### Setting up Auth0
Use the third-party application [Auth0](https://auth0.com/) to implement authentication and role-based access control (**RBAC**).

- Create a new [Auth0](https://auth0.com/) Account
- Select a unique tenant domain
- Create a new, single page web application
- Create a new API
    - in API Settings:
      - Enable RBAC
      - Enable Add Permissions in the Access Token
- Create new API permissions:
    - `get:characters`
    - `get:character`
    - `post:character`
    - `patch:character`
    - `delete:character`
    - `get:cards`
    - `get:card`
    - `post:card`
    - `patch:card`
    - `delete:card`
    - `get:skills`
    - `get:skill`
    - `post:skill`
    - `patch:skill`
    - `delete:skill`
  
- Create new roles for:
    - Contributor
        - can perform all actions
    - Member
        - can perform all `get` actions

- Configure the application variables in `./src/auth/auth.py`:
```py
    AUTH0_DOMAIN = {AUTH0 DOMAIN PREFIX}
    ALGORITHMS = ['RS256']
    API_AUDIENCE = {AUTH0 APP API AUDIENCE}
``` 

## Running the server

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Live API via Heroku

A deployed instance of the API can be found here:

 https://fsnd-capstone.herokuapp.com

Here are a few useful endpoints to test the live application, but keep in mind an authentication token is required to access the application:

> `curl --location --request GET "https://fsnd-capstone.herokuapp.com/characters" -H "Authorization: Bearer <ACCESS_TOKEN>"`

> `curl --location --request GET "https://fsnd-capstone.herokuapp.com/cards" -H "Authorization: Bearer <ACCESS_TOKEN>"`

> `curl --location --request GET "https://fsnd-capstone.herokuapp.com/skills" -H "Authorization: Bearer <ACCESS_TOKEN>"`

## API Reference

Currently, the API only supports basic CRUD operations on the database. If you plan on extending this application it is likely you would want to add additional search and filtering operations.

[View the README.md within ./database for full API Reference.](./database/README.md)

## Authors

Mobile gacha API implemented by Kristoffer Alquiza in part of the Full Stack Web Developer Course at [Udacity](https://www.udacity.com/course/).

## Acknowledgements
This project was completed as part of the Full Stack Web Developer Course at [Udacity](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044). Credit to the Udacity team for providing the course content and the required knowledge to complete this application.