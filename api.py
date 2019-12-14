from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api
from character import Character


class CharacterSimple(Resource):
    def get(self, character_id):
        character = Character.query.filter(
            Character.id == character_id).one_or_none()

        response = jsonify({
            'success': True,
            'character': [character.profile()]
        })
        response.status_code = 200
        return response

    def post(self):
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
