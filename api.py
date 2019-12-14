from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api
from character import Character


class CharacterSimple(Resource):
    @requires_auth('get:characters')
    def get(self, jwt):
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
        selection = Character.query.order_by(Character.id).all()
        characters = [character.profile() for character in selection]

        response = jsonify({
            'success': True,
            'character': characters
        })
        response.status_code = 200
        return response

    @requires_auth('get:character')
    def get(self, character_id, jwt):
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
        character = Character.query.filter(
            Character.id == character_id).one_or_none()

        response = jsonify({
            'success': True,
            'character': [character.profile()]
        })
        response.status_code = 200
        return response

    @requires_auth('post:character')
    def post(self, jwt):
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
            # Name
            name = body.get('name', None)
            # Class Type
            class_type = body.get('class_type', None)
            # Age
            age = body.get('age', None)
            # Weight in kg
            weight = body.get('weight', None)
            # Height in cm
            height = body.get('height', None)
            # Blood Type
            bloodtype = body.get('bloodtype', None)
            # Three Sizes
            three_sizes = body.get('three_sizes', None)
            # Handedness
            handedness = body.get('handedness', None)
            # Hobbies
            hobbies = body.get('hobbies', None)
            # Astrological Sign
            astrological_sign = body.get('astrological_sign', None)

            character = Character(
                name=name,
                class_type=class_type,
                age=age,
                weight=weight,
                height=height,
                bloodtype=bloodtype,
                three_sizes=three_sizes,
                handedness=handedness,
                hobbies=hobbies,
                astrological_sign=astrological_sign
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

    @requires_auth('patch:character')
    def patch(self, character_id, jwt):
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
            # Name
            name = body.get('name', None)
            # Class Type
            class_type = body.get('class_type', None)
            # Age
            age = body.get('age', None)
            # Weight in kg
            weight = body.get('weight', None)
            # Height in cm
            height = body.get('height', None)
            # Blood Type
            bloodtype = body.get('bloodtype', None)
            # Three Sizes
            three_sizes = body.get('three_sizes', None)
            # Handedness
            handedness = body.get('handedness', None)
            # Hobbies
            hobbies = body.get('hobbies', None)
            # Astrological Sign
            astrological_sign = body.get('astrological_sign', None)

            character = Character(
                name=name,
                class_type=class_type,
                age=age,
                weight=weight,
                height=height,
                bloodtype=bloodtype,
                three_sizes=three_sizes,
                handedness=handedness,
                hobbies=hobbies,
                astrological_sign=astrological_sign
            )
            character.update()

            return jsonify({
                'success': True,
                'character': [character.profile()]
            }), 200

        except Exception as e:
            abort(422)

    @requires_auth('delete:character')
    def delete(character_id, jwt):
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
                Character.id == character).one_or_none()

            if character is None:
                abort(404)

            id = character.id
            character.delete()

            return jsonify({
                'success': True,
                'delete': id
            }), 200

        except Exception as e:
            abort(422)


""" Error Handling """

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
