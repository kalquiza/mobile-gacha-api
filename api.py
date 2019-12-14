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
