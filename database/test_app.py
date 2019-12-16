import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models from database.database import setup_db
from database.character import Character
from database.card import Card
from database.skill import Skill
import setup_db, Question, Category


class CachaTestCase(unittest.TestCase):
    """This class represents the gacha test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "gacha_test"
        self.database_path = "postgres://{}/{}".format('', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()