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
member_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1UTTJSREl3UkRNNFJrVTBRVFEwUmpjMk1UazFOek5FUkVVNU1rTkJSVFJFUXpFNE1UWkJPUSJ9.eyJpc3MiOiJodHRwczovL2Rldi0yczFrNmM4NC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjOTA2MDIyYjg4MDQwZTY2Mzc1ZWU3IiwiYXVkIjoiaWRvbCIsImlhdCI6MTU3NjczMDM0NCwiZXhwIjoxNTc2ODE2NzQ0LCJhenAiOiJuZVB0YU5SYWhkZ0t3eDVzZjVxaUZIWnl2Z3FXWkt3NyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmNhcmQiLCJnZXQ6Y2FyZHMiLCJnZXQ6Y2hhcmFjdGVyIiwiZ2V0OmNoYXJhY3RlcnMiLCJnZXQ6c2tpbGwiLCJnZXQ6c2tpbGxzIl19.VV0Gb28MUwVmL54xKdqXMiTUMtxGbDF_8UBy7NyasD0ympNUM5PTEnkpWcdxk033sMcrOUjxCwzPazvPw0aAUG5VLJISDASzknufdakfeRrbdP4IyvRP0SZ6y1iAvUbsj-K4sF6xOgtxYNJHadvR5-bEebAH0g18m7Y5GrvcU85cQww6dzXS16kYaPSc7L8Kt4KGzwv0Cw7Ols13T6XH_TnbKXgkMA5BYyX_2ZbxwG5SpkbxGrEAbJCN0jxokPMJqZ4YCXk6LauRyMY1cGE5I-ni2y9KXZSGMu4hDH_3LVFLUeRisQzXNC1I6T2FxeqRFPt4KhvYot3Sr9RkePmmDw"
contributor_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1UTTJSREl3UkRNNFJrVTBRVFEwUmpjMk1UazFOek5FUkVVNU1rTkJSVFJFUXpFNE1UWkJPUSJ9.eyJpc3MiOiJodHRwczovL2Rldi0yczFrNmM4NC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRjOTA2NDE3MGUzMGYwZTYyNjYwY2I0IiwiYXVkIjoiaWRvbCIsImlhdCI6MTU3NjczMDI4NiwiZXhwIjoxNTc2ODE2Njg2LCJhenAiOiJuZVB0YU5SYWhkZ0t3eDVzZjVxaUZIWnl2Z3FXWkt3NyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNhcmQiLCJkZWxldGU6Y2hhcmFjdGVyIiwiZGVsZXRlOnNraWxsIiwiZ2V0OmNhcmQiLCJnZXQ6Y2FyZHMiLCJnZXQ6Y2hhcmFjdGVyIiwiZ2V0OmNoYXJhY3RlcnMiLCJnZXQ6c2tpbGwiLCJnZXQ6c2tpbGxzIiwicGF0Y2g6Y2FyZCIsInBhdGNoOmNoYXJhY3RlciIsInBhdGNoOnNraWxsIiwicG9zdDpjYXJkIiwicG9zdDpjaGFyYWN0ZXIiLCJwb3N0OnNraWxsIl19.kFic7Q-r4p-RqieiyTA0chtfDFnA43Dv0gH5B7MxxZvl5R6b9L9K8iC4mDkeGGWw76bIAKKi3BHFgizNmBRVQ7BTslBuShTzPx26LW75SE4AyuwjqsRvBFSjne42wGM4XEiuxaFsm5P1XOJNvxO7AqNDLvpdF-15hhHWoZmoRK4ls_a1pCcag4HyOiMdt13q7zJzBBUZqEaBooMnWEn1Iw2WEogVVS-mFiaen1QB2hvjlQWKqGS2S8pbP9ayzyMhbOV6XLQPh2X230b7AgHyHAoNLOmgnb2-WmbP17bttQjjh7joRGfvFCw9DTvj4_3M4PQyWx-vY-ZkhKT1zkOdpQ"


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
                "description": "For the next 5 seconds, score of all notes \
                boosted by +100.0%",
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
                "description": "390 Life Recovery and Score increased by 70% \
                for 8 seconds",
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
                "description": "For the next 5 seconds, score of all notes \
                boosted by +100.0%",
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
                "description": "390 Life Recovery and Score increased by 70% \
                for 8 seconds",
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
