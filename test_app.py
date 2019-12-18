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
member_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1UTTJSREl3UkRNNFJrVTBRVFEwUmpjMk1UazFOek5FUkVVNU1rTkJSVFJFUXpFNE1UWkJPUSJ9.eyJpc3MiOiJodHRwczovL2Rldi0yczFrNmM4NC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjOTA2MDIyYjg4MDQwZTY2Mzc1ZWU3IiwiYXVkIjoiaWRvbCIsImlhdCI6MTU3NjYyNDMzNCwiZXhwIjoxNTc2NzEwNzM0LCJhenAiOiJuZVB0YU5SYWhkZ0t3eDVzZjVxaUZIWnl2Z3FXWkt3NyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmNhcmQiLCJnZXQ6Y2FyZHMiLCJnZXQ6Y2hhcmFjdGVyIiwiZ2V0OmNoYXJhY3RlcnMiLCJnZXQ6c2tpbGwiLCJnZXQ6c2tpbGxzIl19.hnXDkavHpPn1_RF-J-osmB2tTtGCdrZZMwRTJR2DIWufAadqaYcnllSszRwQ7R2KH3JmkSvPjw4fAu7gceHFS3AKpuovQKqo0awiphSY3_OiWist30QNXkQAgLxLgJ8vIKz_rn8gGcbBMend1loU9w0me3RWMLIOxvj9W8RtTw3_SydbrLrxW1J3NWtN4RmXAtk9U8-OhkDS-wrSx_QavNzRNPpUAVzTkGvvb5FcpopuhsySflcs85NTPbUdR3LlJOr1B0U3_wl92MA8vrZESuaKWgfhEa253nvuD76IEmDRQNc5p9m9iyOSzeHjRED1g3-zUABooTMJimJZgwL2vw"
contributor_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1UTTJSREl3UkRNNFJrVTBRVFEwUmpjMk1UazFOek5FUkVVNU1rTkJSVFJFUXpFNE1UWkJPUSJ9.eyJpc3MiOiJodHRwczovL2Rldi0yczFrNmM4NC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjOTA2NDE3MGUzMGYwZTYyNjYwY2I0IiwiYXVkIjoiaWRvbCIsImlhdCI6MTU3NjYyNDI3NiwiZXhwIjoxNTc2NzEwNjc2LCJhenAiOiJuZVB0YU5SYWhkZ0t3eDVzZjVxaUZIWnl2Z3FXWkt3NyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNhcmQiLCJkZWxldGU6Y2hhcmFjdGVyIiwiZGVsZXRlOnNraWxsIiwiZ2V0OmNhcmQiLCJnZXQ6Y2FyZHMiLCJnZXQ6Y2hhcmFjdGVyIiwiZ2V0OmNoYXJhY3RlcnMiLCJnZXQ6c2tpbGwiLCJnZXQ6c2tpbGxzIiwicGF0Y2g6Y2FyZCIsInBhdGNoOmNoYXJhY3RlciIsInBhdGNoOnNraWxsIiwicG9zdDpjYXJkIiwicG9zdDpjaGFyYWN0ZXIiLCJwb3N0OnNraWxsIl19.a_EY2uJ-prA3IA19o_XHTpfKJUSWvL27xqr-s7Gb-0kscAZDBeg8MFq-bqPPFjw7mwX9OGntQHVuffJMVNAcPRJFCz4VhF9B_xzHk8ySsDZCMmY6M-xO8OGffekcnR5ef3Tim3ZkYgWvWXZySXxJEnnAqmrrLjtTZ-oaVSIRQV6hhwrN4_WDmSTuud3VRTPfOyPrPHvZXsh0GxIuXBC4dmciwJ0JAF8Dhh0fm48YO7Ef82NIqEkHDd6GBe1AtKIlURqGweBOwchRDymFVmXm_SopYtZoQfh4JuHJ6wJeJ0IhnMFcHcb5BZC6nf9iDW18Q88ZmDLgwd3gcp0qotBxlg"


class GachaTestCase(unittest.TestCase):
    """This class represents the gacha test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_db_test"
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
    def test_get_characters_member_auth(self):
        res = self.client().get(
            '/characters',
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ GET /characters/<id>"""
    def test_get_character_member_auth(self):
        character_id = 1
        res = self.client().get(
            '/characters/{}'.format(character_id),
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ POST /characters"""
    def test_post_character_member_auth(self):
        res = self.client().post(
            '/characters',
            headers={'Authorization': "Bearer {0}".format(member_token)},
            json={
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
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ PATCH /characters/<id>"""
    def test_patch_character_member_auth(self):
        character_id = 8
        res = self.client().patch(
            '/characters/{}'.format(character_id),
            headers={'Authorization': "Bearer {0}".format(member_token)},
            json={
                "hobbies": "Web Development",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ DELETE /characters/<id>"""
    def test_delete_character_member_auth(self):
        character_id = 2
        res = self.client().delete(
            '/characters/{}'.format(character_id),
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Contributor authentication
    # ------------------------------------------------------------------------#
    """ GET /characters"""
    def test_get_characters_contributor_auth(self):
        res = self.client().get(
            '/characters',
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ GET /characters/<id>"""
    def test_get_character_contributor_auth(self):
        character_id = 1
        res = self.client().get(
            '/characters/{}'.format(character_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    """ POST /characters"""
    def test_post_character_contributor_auth(self):
        res = self.client().post(
            '/characters',
            headers={'Authorization': "Bearer {0}".format(contributor_token)},
            json={
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
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """ PATCH /characters/<id>"""
    def test_patch_character_contributor_auth(self):
        character_id = 1
        res = self.client().patch(
            '/characters/{}'.format(character_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)},
            json={
                "hobbies": "Web Development",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """ DELETE /characters/<id>"""
    def test_delete_character_contributor_auth(self):
        character_id = 2
        res = self.client().delete(
            '/characters/{}'.format(character_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], character_id)

    # Other Errors
    # ------------------------------------------------------------------------#
    """ 422 Unprocessable"""
    def test_error_unprocessable(self):
        res = self.client().post(
            '/characters',
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """ 404 Resource not found"""
    def test_error_unprocessable_resource_not_found(self):
        character_id = 10000
        res = self.client().get(
            '/characters/{}'.format(character_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # ------------------------------------------------------------------------#
    # Card
    # ------------------------------------------------------------------------#

    # No authentication
    # ------------------------------------------------------------------------#
    """ GET /cards"""
    def test_get_cards_no_auth(self):
        res = self.client().get('/cards')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ GET /cards/<id>"""
    def test_get_card_no_auth(self):
        card_id = 1
        res = self.client().patch('/cards/{}'.format(card_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Member authentication
    # ------------------------------------------------------------------------#
    """ GET /cards"""
    def test_get_cards_member_auth(self):
        res = self.client().get(
            '/cards',
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['card'])

    """ GET /cards/<id>"""
    def test_get_card_member_auth(self):
        card_id = 1
        res = self.client().get(
            '/cards/{}'.format(card_id),
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['card'])

    """ POST /cards"""
    def test_post_card_member_auth(self):
        res = self.client().post(
            '/cards',
            headers={'Authorization': "Bearer {0}".format(member_token)},
            json={
                "name": "Diva of the Birdcage",
                "character": 7,
                "skill": 8,
                "rarity": "4-star",
                "stat_1": "8491",
                "stat_2": "4505",
                "stat_3": "5832",
                "stat_4": "18828",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ PATCH /cards/<id>"""
    def test_patch_card_member_auth(self):
        card_id = 4
        res = self.client().patch(
            '/cards/{}'.format(card_id),
            headers={'Authorization': "Bearer {0}".format(member_token)},
            json={
                "skill": 3,
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ DELETE /cards/<id>"""
    def test_delete_card_member_auth(self):
        card_id = 2
        res = self.client().delete(
            '/cards/{}'.format(card_id),
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Contributor authentication
    # ------------------------------------------------------------------------#
    """ GET /cards"""
    def test_get_cards_contributor_auth(self):
        res = self.client().get(
            '/cards',
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['card'])

    """ GET /cards/<id>"""
    def test_get_card_contributor_auth(self):
        card_id = 1
        res = self.client().get(
            '/cards/{}'.format(card_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['card'])

    """ POST /cards"""
    def test_post_card_contributor_auth(self):
        res = self.client().post(
            '/cards',
            headers={'Authorization': "Bearer {0}".format(contributor_token)},
            json={
                "name": "Diva of the Birdcage",
                "character": 7,
                "skill": 8,
                "rarity": "4-star",
                "stat_1": "8491",
                "stat_2": "4505",
                "stat_3": "5832",
                "stat_4": "18828",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """ PATCH /cards/<id>"""
    def test_patch_card_contributor_auth(self):
        card_id = 4
        res = self.client().patch(
            '/cards/{}'.format(card_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)},
            json={
                "skill": 3,
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """ DELETE /cards/<id>"""
    def test_delete_card_contributor_auth(self):
        card_id = 2
        res = self.client().delete(
            '/cards/{}'.format(card_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], card_id)

    # Other Errors
    # ------------------------------------------------------------------------#
    """ 422 Unprocessable"""
    def test_error_unprocessable(self):
        res = self.client().post(
            '/cards',
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """ 404 Resource not found"""
    def test_error_unprocessable_resource_not_found(self):
        card_id = 10000
        res = self.client().get(
            '/cards/{}'.format(card_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # ------------------------------------------------------------------------#
    # Skill
    # ------------------------------------------------------------------------#

    # No authentication
    # ------------------------------------------------------------------------#
    """ GET /skills"""
    def test_get_skills_no_auth(self):
        res = self.client().get('/skills')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ GET /skills/<id>"""
    def test_get_skill_no_auth(self):
        skill_id = 1
        res = self.client().patch('/skills/{}'.format(skill_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Member authentication
    # ------------------------------------------------------------------------#
    """ GET /skills"""
    def test_get_skills_member_auth(self):
        res = self.client().get(
            '/skills',
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

    """ GET /skills/<id>"""
    def test_get_skill_member_auth(self):
        skill_id = 1
        res = self.client().get(
            '/skills/{}'.format(skill_id),
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

    """ POST /skills"""
    def test_post_skill_member_auth(self):
        res = self.client().post(
            '/skills',
            headers={'Authorization': "Bearer {0}".format(member_token)},
            json={
                "name": "Violent shout",
                "description": "For the next 5 seconds, score of all notes boosted by +100.0%",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ PATCH /skills/<id>"""
    def test_patch_skill_member_auth(self):
        skill_id = 8
        res = self.client().patch(
            '/skills/{}'.format(skill_id),
            headers={'Authorization': "Bearer {0}".format(member_token)},
            json={
                "description": "390 Life Recovery and Score increased by 70% for 8 seconds",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """ DELETE /skills/<id>"""
    def test_delete_skill_member_auth(self):
        skill_id = 2
        res = self.client().delete(
            '/skills/{}'.format(skill_id),
            headers={'Authorization': "Bearer {0}".format(member_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Contributor authentication
    # ------------------------------------------------------------------------#
    """ GET /skills"""
    def test_get_skills_contributor_auth(self):
        res = self.client().get(
            '/skills',
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

    """ GET /skills/<id>"""
    def test_get_skill_contributor_auth(self):
        skill_id = 1
        res = self.client().get(
            '/skills/{}'.format(skill_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

    """ POST /skills"""
    def test_post_skill_contributor_auth(self):
        res = self.client().post(
            '/skills',
            headers={'Authorization': "Bearer {0}".format(contributor_token)},
            json={
                "name": "Violent shout",
                "description": "For the next 5 seconds, score of all notes boosted by +100.0%",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """ PATCH /skills/<id>"""
    def test_patch_skill_contributor_auth(self):
        skill_id = 1
        res = self.client().patch(
            '/skills/{}'.format(skill_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)},
            json={
                "description": "390 Life Recovery and Score increased by 70% for 8 seconds",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """ DELETE /skills/<id>"""
    def test_delete_skill_contributor_auth(self):
        skill_id = 2
        res = self.client().delete(
            '/skills/{}'.format(skill_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], skill_id)

    # Other Errors
    # ------------------------------------------------------------------------#
    """ 422 Unprocessable"""
    def test_error_unprocessable(self):
        res = self.client().post(
            '/skills',
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """ 404 Resource not found"""
    def test_error_unprocessable_resource_not_found(self):
        skill_id = 10000
        res = self.client().get(
            '/skills/{}'.format(skill_id),
            headers={'Authorization': "Bearer {0}".format(contributor_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# ----------------------------------------------------------------------------#
# Launch
# ----------------------------------------------------------------------------#

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
