from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Types(db.Model):
    __tablename__ = 'frog_types'
    type_id = db.Column('id', db.Integer, primary_key=True)
    type_name = db.Column(db.Text)
    type_img = db.Column(db.Text)

class Places(db.Model):
    __tablename__ = 'places'
    place_id = db.Column('id', db.Integer, primary_key=True)
    place_name = db.Column(db.Text)
    place_img = db.Column(db.Text)

class Friends(db.Model):
    __tablename__ = 'friends'
    friend_id = db.Column('id', db.Integer, primary_key=True)
    friend_name = db.Column(db.Text)
    friend_img = db.Column(db.Text)

class Frogs(db.Model):
    __tablename__ = 'frogs'
    frog_id = db.Column('id', db.Integer, primary_key=True)
    human_name = db.Column(db.Text)
    frog_name = db.Column(db.Text)
    frog_type_id = db.Column('type_id', db.Integer, ForeignKey('frog_types.id'))
    frog_type = db.relationship('Types')
    place_id = db.Column('place_id', db.Integer, ForeignKey('places.id'))
    place = db.relationship('Places')

class FrogToFriend(db.Model):
    __tablename__ = 'frog_to_friend'
    __table_args__ = (PrimaryKeyConstraint('frog_id', 'friend_id'),)

    frog_id = db.Column('frog_id', db.Integer, ForeignKey('frogs.id'))
    friend_id = db.Column('friend_id', db.Integer, ForeignKey('friends.id'))

