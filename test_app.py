import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.database import setup_db
from database.character import Character
from database.card import Card
from database.skill import Skill

# ----------------------------------------------------------------------------#
# Setup
# ----------------------------------------------------------------------------#

""" Provide recent tokens for member and contributor roles.
    Tests will fail if token is invalid or expired.
"""
member_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1UTTJSREl3UkRNNFJrVTBRVFEwUmpjMk1UazFOek5FUkVVNU1rTkJSVFJFUXpFNE1UWkJPUSJ9.eyJpc3MiOiJodHRwczovL2Rldi0yczFrNmM4NC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjOTA2NDE3MGUzMGYwZTYyNjYwY2I0IiwiYXVkIjoiaWRvbCIsImlhdCI6MTU3NjU0MTQ0OSwiZXhwIjoxNTc2NTQ4NjQ5LCJhenAiOiJuZVB0YU5SYWhkZ0t3eDVzZjVxaUZIWnl2Z3FXWkt3NyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNhcmQiLCJkZWxldGU6Y2hhcmFjdGVyIiwiZGVsZXRlOnNraWxsIiwiZ2V0OmNhcmQiLCJnZXQ6Y2FyZHMiLCJnZXQ6Y2hhcmFjdGVyIiwiZ2V0OmNoYXJhY3RlcnMiLCJnZXQ6c2tpbGwiLCJnZXQ6c2tpbGxzIiwicGF0Y2g6Y2FyZCIsInBhdGNoOmNoYXJhY3RlciIsInBhdGNoOnNraWxsIiwicG9zdDpjYXJkIiwicG9zdDpjaGFyYWN0ZXIiLCJwb3N0OnNraWxsIl19.puE5WCkfpSXCB79deBRYnS-bEQqDcjGFZ3qhbehY9f2_LHPbsV13j7yocgfQfGpw9mFfI4kWb_QOb_3vS3aqQNhAqc3YourS4yv4qT7LVCJJsFLrqRjXxgC4vQULEb9GivbhYhl1IimLpFizUbTme3ixDNuK9SHd-bCYZuivytSDZDo3HXTcArIUTMNJT9bo3qqLs4n4F7NswY0mciT-0oVR6UJtF9f2hgsogfd21FyBy_nRRMRdrUz1Eet5CF7Uex6q3-LO4sYhlHePk2YrRqb28Uf3vQf3BlCC00PeboxxUl0PCMmt6MFYufT4-WRPban9ah43gKqa-697fUzPXw"
contributor_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1UTTJSREl3UkRNNFJrVTBRVFEwUmpjMk1UazFOek5FUkVVNU1rTkJSVFJFUXpFNE1UWkJPUSJ9.eyJpc3MiOiJodHRwczovL2Rldi0yczFrNmM4NC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjOTA2MDIyYjg4MDQwZTY2Mzc1ZWU3IiwiYXVkIjoiaWRvbCIsImlhdCI6MTU3NjU0MTM3MiwiZXhwIjoxNTc2NTQ4NTcyLCJhenAiOiJuZVB0YU5SYWhkZ0t3eDVzZjVxaUZIWnl2Z3FXWkt3NyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNhcmQiLCJkZWxldGU6Y2hhcmFjdGVyIiwiZGVsZXRlOnNraWxsIiwiZ2V0OmNhcmQiLCJnZXQ6Y2FyZHMiLCJnZXQ6Y2hhcmFjdGVyIiwiZ2V0OmNoYXJhY3RlcnMiLCJnZXQ6c2tpbGwiLCJnZXQ6c2tpbGxzIiwicGF0Y2g6Y2FyZCIsInBhdGNoOmNoYXJhY3RlciIsInBhdGNoOnNraWxsIiwicG9zdDpjYXJkIiwicG9zdDpjaGFyYWN0ZXIiLCJwb3N0OnNraWxsIl19.LLDfv9Fk2DTbbC96AUZ8jaqA0vTYt6NELy14KRZoZZ9yUqx16ATFD_w4seydAoFOGAS11O66zgMoaNzWN7138C0CXBoCI4eNJxW7XM_auzJ5fBfQGjLdKBbUeAchRfJpHh5dP0PGJQ9VuclJy9Z5oUqkJhl_4P5c9SOQwCq9on8PMTAuj2cPL1Oxhesm2LXzyjWLs3S_Fg9v2zw4m2Nuo3a_Yxds0ldN3ZgTc6mnE7sykClqpbF_mygDnEkMaJd5O3eFJlbIKn01wPxi1vYM38tjhUyXBpILU7Y8-c0KVJiNz7WbkCseLFDvp3g6C1vasLAJxnPIxO2ZEL6J4LgmPw"


class GachaTestCase(unittest.TestCase):
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

    # ------------------------------------------------------------------------#
    # Tests
    # ------------------------------------------------------------------------#

    # ------------------------------------------------------------------------#
    # Character
    # ------------------------------------------------------------------------#

    # No authentication
    # ------------------------------------------------------------------------#
    """ GET /characters"""
    def test_get_characters_no_auth(self):
        res = self.client().get('/characters')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ GET /characters/<id>"""
    def test_get_character_no_auth(self):
        character_id = 1
        res = self.client().patch('/characters/{}'.format(character_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Member authentication
    # ------------------------------------------------------------------------#
    """ GET /characters"""
    def test_characters_member_auth(self):
        res = self.client().get('/characters', headers={'Authorization': "Bearer {0}".format(member_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ GET /characters/<id>"""
    def get_character_member_auth(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': member_token
        }
        character_id = 1
        res = self.client().get('/characters/{}'.format(character_id))
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ POST /characters"""
    def post_character_member_auth(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': member_token
        }
        res = self.client().post('/characters', json={
            "name": "Ohishi Izumi",
            "age": "15",
            "height": "157 cm",
            "weight": "41 kg",
            "birthday": "November 11th",
            "astrological_sign": "Scorpio",
            "bloodtype": "A",
            "three_sizes": "83/55/82",
            "handedness": "Right",
            "hobbies": "Programming",
            "class_type": "Cool"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ PATCH /characters/<id>"""
    def patch_character_member_auth(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': member_token
        }
        character_id = 1
        res = self.client().patch('/characters/{}'.format(character_id), json={
            "name": "Ohishi Izumi",
            "age": "15",
            "height": "157 cm",
            "weight": "41 kg",
            "birthday": "November 11th",
            "astrological_sign": "Scorpio",
            "bloodtype": "A",
            "three_sizes": "83/55/82",
            "handedness": "Right",
            "hobbies": "Web Development",
            "class_type": "Cool"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ DELETE /characters/<id>"""
    def delete_character_member_auth(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': member_token
        }
        character_id = 1
        res = self.client().delete('/characters/{}'.format(character_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Contributor authentication
    # ------------------------------------------------------------------------#
    """ GET /characters"""
    def get_characters_contributor_auth(self):
        # header
        res = self.client().get('/characters')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ GET /characters/<id>"""
    def get_character_contributor_auth(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': contributor_token
        }
        character_id = 1
        res = get.client().get('/characters/{}'.format(character_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ POST /characters"""
    def post_character_contributor_auth(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': contributor_token
        }
        res = self.client().patch('/characters/{}'.format(character_id), json={
            "name": "Ohishi Izumi",
            "age": "15",
            "height": "157 cm",
            "weight": "41 kg",
            "birthday": "November 11th",
            "astrological_sign": "Scorpio",
            "bloodtype": "A",
            "three_sizes": "83/55/82",
            "handedness": "Right",
            "hobbies": "Web Development",
            "class_type": "Cool"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ PATCH /characters/<id>"""
    def patch_character_contributor_auth(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': contributor_token
        }
        character_id = 1
        res = self.client().patch('/characters/{}'.format(character_id), json={

        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'], True)

    """ DELETE /characters/<id>"""
    def delete_character_contributor_auth(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': contributor_token
        }
        character_id = 1
        res = self.client().delete('/characters/{}'.format(character_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], character_id)

    # Other Errors
    # ------------------------------------------------------------------------#
    """ 422 Unprocessable"""
    def error_unprocessable(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': contributor_token
        }
        character_id = 10000
        res = self.client().patch('/characters/{}'.format(character_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """ 404 Resource not found"""
    def error_unprocessable_resource_not_found(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': contributor_token
        }
        res = self.client().delete('/characters')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# ----------------------------------------------------------------------------#
# Launch
# ----------------------------------------------------------------------------#

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
