import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from .database import db

'''
Character

'''


class Character(db.Model):
    __tablename__ = 'Character'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # Name
    name = db.Column(String(80), unique=True)
    # Age
    age = db.Column(String(80))
    # Height in cm
    height = db.Column(String(80))
    # Weight in kg
    weight = db.Column(String(80))
    # Birthday
    birthday = db.Column(String(80))
    # Astrological Sign
    astrological_sign = db.Column(db.String(80))
    # Blood Type
    bloodtype = db.Column(String(80))
    # Three Sizes
    three_sizes = db.Column(String(80))
    # Handedness
    handedness = db.Column(String(80))
    # Hobbies
    hobbies = db.Column(db.String(80))
    # Class Type
    class_type = db.Column(String(80))

    '''
    profile()
        profile of the character model
    '''
    def profile(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'birthday': self.birthday,
            'astrological_sign': self.astrological_sign,
            'bloodtype': self.bloodtype,
            'three_sizes': self.three_sizes,
            'handedness': self.handedness,
            'hobbies': self.hobbies,
            'class_type': self.class_type,
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            character = Character(name=req_name, field=req_field, ...)
            character.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model in a database
        the model must exist in the database
        EXAMPLE
            character = Character(name=req_name, field=req_field, ...)
            character.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a model into a database
        the model must exist in the database
        EXAMPLE
            character = Character.query.filter(
                Character.id == id).one_or_none()
            character.name = 'Izumi'
            character.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.profile())
