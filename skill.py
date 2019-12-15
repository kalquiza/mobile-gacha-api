import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from database import db

'''
Skill

'''


class Skill(db.Model):
    __tablename__ = 'Skill'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # Name
    name = db.Column(String(120), nullable=False)
    # Type Bonus
    type_bonus = db.Column(String(120))
    # Stat Bonus
    stat_bonus = db.Column(String(120))
    # Multiplier
    multiplier = db.Column(db.Integer)

    '''
    info()
        info of the skill model
    '''
    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'type_bonus': self.type_bonus,
            'stat_bonus': self.stat_bonus,
            'multiplier': self.multiplier
            }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            skill = Skill(name=req_name, field=req_field, ...)
            skill.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model in a database
        the model must exist in the database
        EXAMPLE
            skill = Skill(name=req_name, field=req_field, ...)
            skill.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a model into a database
        the model must exist in the database
        EXAMPLE
            skill = Skill.query.filter(Skill.id == id).one_or_none()
            skill.name = 'Kirari'
            skill.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.info())
