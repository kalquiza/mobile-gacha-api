import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Resource, Api
from auth.auth import AuthError, requires_auth
from database.database import db_drop_and_create_all, setup_db
from database.character import Character
from database.card import Card
from database.skill import Skill


app = Flask(__name__)


def create_app(test_config=None):
    # create and configure the app
    setup_db(app)
    CORS(app)

    return app

# ----------------------------------------------------------------------------#
# Launch
# ----------------------------------------------------------------------------#


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)


# ----------------------------------------------------------------------------#
# Routes
# ----------------------------------------------------------------------------#

# Characters
# ----------------------------------------------------------------------------#
@app.route('/characters', methods=['GET'])
@requires_auth('get:characters')
def get_characters(jwt):
    """GET /characters

    A public endpoint that retrieves the list of characters. Requires the
    'get:characters' permission.

    Args:
        jwt: a json web token (string).

    Returns:
        A status code 200 and json {"success": True, "characters":
        characters} where characters is the list of characters in the
        characters.profile() representation or appropriate status code
        indicating reason for failure.
    """
    try:
        selection = Character.query.order_by(Character.id).all()
        characters = [character.profile() for character in selection]

        response = jsonify({
            'success': True,
            'character': characters
        })
        response.status_code = 200
        return response
    except Exception as e:
        abort(404)


@app.route('/characters/<int:character_id>', methods=['GET'])
@requires_auth('get:character')
def get_character(jwt, character_id):
    """GET /characters/<id>

    A public endpoint that retrieves the character for the corresponding
    row for <id>. Requires the 'get:character' permission.

    Args:
        jwt: a json web token (string).
        character_id: where <character_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "character":
        character} where character is the character in the
        character.profile() representation or appropriate status code
        indicating reason for failure.
    """
    try:
        character = Character.query.filter(
            Character.id == character_id).one_or_none()

        response = jsonify({
            'success': True,
            'character': [character.profile()]
        })
        response.status_code = 200
        return response
    except Exception as e:
        abort(404)


@app.route('/characters', methods=['POST'])
@requires_auth('post:character')
def create_character(jwt):
    """POST /characters

    An endpoint that creates a new row in the characters table. Requires
    the 'post:character' permission.

    Args:
        jwt: a json web token (string).
        character_id: where <character_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "character":
        character} where character is an array containing only the newly
        created character in the character.profile() representation or
        appropriate status code indicating reason for failure.
    """
    try:
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        height = body.get('height', None)
        weight = body.get('weight', None)
        birthday = body.get('birthday', None)
        astrological_sign = body.get('astrological_sign', None)
        bloodtype = body.get('bloodtype', None)
        three_sizes = body.get('three_sizes', None)
        handedness = body.get('handedness', None)
        hobbies = body.get('hobbies', None)
        class_type = body.get('class_type', None)

        character = Character(
            name=name,
            age=age,
            height=height,
            weight=weight,
            birthday=birthday,
            astrological_sign=astrological_sign,
            bloodtype=bloodtype,
            three_sizes=three_sizes,
            handedness=handedness,
            hobbies=hobbies,
            class_type=class_type,
        )
        character.insert()

        response = jsonify({
            'success': True,
            'character': [character.profile()]
        })
        response.status_code = 200
        return response

    except Exception as e:
        abort(422)


@app.route('/characters/<int:character_id>', methods=['PATCH'])
@requires_auth('patch:character')
def update_character(jwt, character_id):
    """PATCH /characters/<id>

    An endpoint that updates the corresponding row for <id>. Requires the
    'patch:character' permission.

    Args:
        jwt: a json web token (string).
        character_id: where <character_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "character":
        character} where character is an array containing only the updated
        character in the character.profile() representation or appropriate
        status code indicating reason for failure.
    """
    try:
        character = Character.query.filter(
            Character.id == character_id).one_or_none()

        if character is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        height = body.get('height', None)
        weight = body.get('weight', None)
        birthday = body.get('birthday', None)
        astrological_sign = body.get('astrological_sign', None)
        bloodtype = body.get('bloodtype', None)
        three_sizes = body.get('three_sizes', None)
        handedness = body.get('handedness', None)
        hobbies = body.get('hobbies', None)
        class_type = body.get('class_type', None)

        character = Character(
            name=name,
            age=age,
            height=height,
            weight=weight,
            birthday=birthday,
            astrological_sign=astrological_sign,
            bloodtype=bloodtype,
            three_sizes=three_sizes,
            handedness=handedness,
            hobbies=hobbies,
            class_type=class_type,
        )
        character.update()

        return jsonify({
            'success': True,
            'character': [character.profile()]
        }), 200

    except Exception as e:
        abort(422)


@app.route('/characters/<int:character_id>', methods=['DELETE'])
@requires_auth('delete:character')
def delete_character(jwt, character_id):
    """
        DELETE /characters/<id>:
            An endpoint that deletes the corresponding row for <id>.
            Requires the 'delete:character' permission.

        Args:
            jwt: a json web token (string).
            character_id: where <character_id> is the existing model id
            (int).

        Returns:
            A status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record or appropriate status
            code indicating reason for failure.
    """
    try:
        character = Character.query.filter(
            Character.id == character_id).one_or_none()

        if character is None:
            abort(404)

        char_id = character.id
        character.delete()

        return jsonify({
            'success': True,
            'delete': char_id
        }), 200

    except Exception as e:
        abort(422)

# Cards
# ----------------------------------------------------------------------------#
@app.route('/cards', methods=['GET'])
@requires_auth('get:cards')
def get_cards(jwt):
    """GET /cards

    A public endpoint that retrieves the list of cards. Requires the
    'get:cards' permission.

    Args:
        jwt: a json web token (string).

    Returns:
        A status code 200 and json {"success": True, "cards":
        cards} where cards is the list of cards in the
        cards.info() representation or appropriate status code
        indicating reason for failure.
    """
    try:
        selection = Card.query.order_by(Card.id).all()
        cards = [card.info() for card in selection]

        response = jsonify({
            'success': True,
            'card': cards
        })
        response.status_code = 200
        return response
    except Exception as e:
        abort(404)


@app.route('/cards/<int:card_id>', methods=['GET'])
@requires_auth('get:card')
def get_card(jwt, card_id):
    """GET /cards/<id>

    A public endpoint that retrieves the card for the corresponding
    row for <id>. Requires the 'get:card' permission.

    Args:
        jwt: a json web token (string).
        card_id: where <card_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "card":
        card} where card is the card in the
        card.info() representation or appropriate status code
        indicating reason for failure.
    """
    try:
        card = Card.query.filter(
            Card.id == card_id).one_or_none()

        response = jsonify({
            'success': True,
            'card': [card.info()]
        })
        response.status_code = 200
        return response
    except Exception as e:
        abort(404)


@app.route('/cards', methods=['POST'])
@requires_auth('post:card')
def create_card(jwt):
    """POST /cards

    An endpoint that creates a new row in the cards table. Requires
    the 'post:card' permission.

    Args:
        jwt: a json web token (string).
        card_id: where <card_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "card":
        card} where card is an array containing only the newly
        created card in the card.info() representation or
        appropriate status code indicating reason for failure.
    """
    try:
        body = request.get_json()
        name = body.get('name', None)
        character = body.get('character', None)
        skill = body.get('skill', None)
        rarity = body.get('rarity', None)
        stat_1 = body.get('stat_1', None)
        stat_2 = body.get('stat_2', None)
        stat_3 = body.get('stat_3', None)
        stat_4 = body.get('stat_4', None)

        card = Card(
            name=name,
            character=character,
            skill=skill,
            rarity=rarity,
            stat_1=stat_1,
            stat_2=stat_2,
            stat_3=stat_3,
            stat_4=stat_4
        )
        card.insert()

        response = jsonify({
            'success': True,
            'card': [card.info()]
        })
        response.status_code = 200
        return response

    except Exception as e:
        abort(422)


@app.route('/cards/<int:card_id>', methods=['PATCH'])
@requires_auth('patch:card')
def update_card(jwt, card_id):
    """PATCH /cards/<id>

    An endpoint that updates the corresponding row for <id>. Requires the
    'patch:card' permission.

    Args:
        jwt: a json web token (string).
        card_id: where <card_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "card":
        card} where card is an array containing only the updated
        card in the card.info() representation or appropriate
        status code indicating reason for failure.
    """
    try:
        card = Card.query.filter(
            Card.id == card_id).one_or_none()

        if card is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        character = body.get('character', None)
        skill = body.get('skill', None)
        rarity = body.get('rarity', None)
        stat_1 = body.get('stat_1', None)
        stat_2 = body.get('stat_2', None)
        stat_3 = body.get('stat_3', None)
        stat_4 = body.get('stat_4', None)

        card = Card(
            name=name,
            character=character,
            skill=skill,
            rarity=rarity,
            stat_1=stat_1,
            stat_2=stat_2,
            stat_3=stat_3,
            stat_4=stat_4
        )
        card.update()

        return jsonify({
            'success': True,
            'card': [card.info()]
        }), 200

    except Exception as e:
        abort(422)


@app.route('/cards/<int:card_id>', methods=['DELETE'])
@requires_auth('delete:card')
def delete_card(jwt, card_id):
    """
        DELETE /cards/<id>:
            An endpoint that deletes the corresponding row for <id>.
            Requires the 'delete:card' permission.

        Args:
            jwt: a json web token (string).
            card_id: where <card_id> is the existing model id
            (int).

        Returns:
            A status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record or appropriate status
            code indicating reason for failure.
    """
    try:
        card = Card.query.filter(
            Card.id == card_id).one_or_none()

        if card is None:
            abort(404)

        card_id = card.id
        card.delete()

        return jsonify({
            'success': True,
            'delete': card_id
        }), 200

    except Exception as e:
        abort(422)


# Skills
# ----------------------------------------------------------------------------#
@app.route('/skills', methods=['GET'])
@requires_auth('get:skills')
def get_skills(jwt):
    """GET /skills

    A public endpoint that retrieves the list of skills. Requires the
    'get:skills' permission.

    Args:
        jwt: a json web token (string).

    Returns:
        A status code 200 and json {"success": True, "skills":
        skills} where skills is the list of skills in the
        skills.info() representation or appropriate status code
        indicating reason for failure.
    """
    try:
        selection = Skill.query.order_by(Skill.id).all()
        skills = [skill.info() for skill in selection]

        response = jsonify({
            'success': True,
            'skill': skills
        })
        response.status_code = 200
        return response
    except Exception as e:
        abort(404)


@app.route('/skills/<int:skill_id>', methods=['GET'])
@requires_auth('get:skill')
def get_skill(jwt, skill_id):
    """GET /skills/<id>

    A public endpoint that retrieves the skill for the corresponding
    row for <id>. Requires the 'get:skill' permission.

    Args:
        jwt: a json web token (string).
        skill_id: where <skill_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "skill":
        skill} where skill is the skill in the
        skill.info() representation or appropriate status code
        indicating reason for failure.
    """
    try:
        skill = Skill.query.filter(
            Skill.id == skill_id).one_or_none()

        response = jsonify({
            'success': True,
            'skill': [skill.info()]
        })
        response.status_code = 200
        return response
    except Exception as e:
        abort(404)


@app.route('/skills', methods=['POST'])
@requires_auth('post:skill')
def create_skill(jwt):
    """POST /skills

    An endpoint that creates a new row in the skills table. Requires
    the 'post:skill' permission.

    Args:
        jwt: a json web token (string).
        skill_id: where <skill_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "skill":
        skill} where skill is an array containing only the newly
        created skill in the skill.info() representation or
        appropriate status code indicating reason for failure.
    """
    try:
        body = request.get_json()
        name = body.get('name', None)
        desc = body.get('desc', None)

        skill = Skill(
            name=name,
            desc=desc
        )
        skill.insert()

        response = jsonify({
            'success': True,
            'skill': [skill.info()]
        })
        response.status_code = 200
        return response

    except Exception as e:
        abort(422)


@app.route('/skills/<int:skill_id>', methods=['PATCH'])
@requires_auth('patch:skill')
def update_skill(jwt, skill_id):
    """PATCH /skills/<id>

    An endpoint that updates the corresponding row for <id>. Requires the
    'patch:skill' permission.

    Args:
        jwt: a json web token (string).
        skill_id: where <skill_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "skill":
        skill} where skill is an array containing only the updated
        skill in the skill.info() representation or appropriate
        status code indicating reason for failure.
    """
    try:
        skill = Skill.query.filter(
            Skill.id == skill_id).one_or_none()

        if skill is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        desc = body.get('desc', None)

        skill = Skill(
            name=name,
            desc=desc
        )
        skill.update()

        return jsonify({
            'success': True,
            'skill': [skill.info()]
        }), 200

    except Exception as e:
        abort(422)


@app.route('/skills/<int:skill_id>', methods=['DELETE'])
@requires_auth('delete:skill')
def delete_skill(jwt, skill_id):
    """
        DELETE /skills/<id>:
            An endpoint that deletes the corresponding row for <id>.
            Requires the 'delete:skill' permission.

        Args:
            jwt: a json web token (string).
            skill_id: where <skill_id> is the existing model id
            (int).

        Returns:
            A status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record or appropriate status
            code indicating reason for failure.
    """
    try:
        skill = Skill.query.filter(
            Skill.id == skill_id).one_or_none()

        if skill is None:
            abort(404)

        skill_id = skill.id
        skill.delete()

        return jsonify({
            'success': True,
            'delete': skill_id
        }), 200

    except Exception as e:
        abort(422)

# ----------------------------------------------------------------------------#
# Error Handling
# ----------------------------------------------------------------------------#


"""
Error handling for unprocessable entity
"""
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


"""
Error handler for the requested resource could not be found
"""
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


"""
Error handler for when authentication is required and has failed or has not
yet been provided
"""
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401
