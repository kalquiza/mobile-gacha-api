import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Resource, Api
from database import db_drop_and_create_all, setup_db
from api import CharacterSimple


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)

    api = Api(app)
    api.add_resource(
        CharacterSimple, '/characters/<string:character_id>', '/characters/'
    )

    CORS(app)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
