import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from .database import db

'''
Card

'''


class Card(db.Model):
    __tablename__ = 'Card'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # Card Name
    name = db.Column(String(80), nullable=False)
    # Card Character
    character = db.Column(db.Integer, db.ForeignKey('Character.id'))
    # Skill
    skill = db.Column(db.Integer, db.ForeignKey('Skill.id'))
    # Rarity
    rarity = db.Column(String(80), nullable=False)
    # Stat 1
    stat_1 = db.Column(db.Integer, nullable=False)
    # Stat 2
    stat_2 = db.Column(db.Integer, nullable=False)
    # Stat 3
    stat_3 = db.Column(db.Integer, nullable=False)
    # Stat 4
    stat_4 = db.Column(db.Integer, nullable=False)

    '''
    info()
        info of the card model
    '''
    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'character': self.character.profile(),
            'skill': self.skill.info(),
            'rarity': self.rarity,
            'stat_1': self.stat_1,
            'stat_2': self.stat_2,
            'stat_3': self.stat_3,
            'stat_4': self.stat_4
            }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            card = Card(name=req_name, field=req_field, ...)
            card.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model in a database
        the model must exist in the database
        EXAMPLE
            card = Card(name=req_name, field=req_field, ...)
            card.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a model into a database
        the model must exist in the database
        EXAMPLE
            card = Card.query.filter(Card.id == id).one_or_none()
            card.name = 'Kirari'
            card.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.info())
