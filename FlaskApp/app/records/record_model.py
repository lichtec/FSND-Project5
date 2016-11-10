from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from app import db


class Base(db.Model):
    # Base model for subsequent models
    # Auth model also uses this base model

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())


class Genre(Base):

    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String, nullable=True)
    genre_image = db.Column(db.VARCHAR(200), nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.genre_name,
            'description': self.description,
            'image':   self.genre_image,
        }

    # New instance instantiation procedure
        def __init__(self, genre_name, description, genre_image):
            self.genre_name = genre_name
            self.description = description
        self.genre_image = genre_image

    def __repr__(self):
        return '<Genre %r>' % (self.genre_name)


class Artist(Base):

    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(250), nullable=False)
    genre_id = db.Column(db.Integer, ForeignKey('genre.id'), nullable=True)
    genre = db.relationship(Genre)
    artist_image = db.Column(db.VARCHAR(200), nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.artist_name,
            'id': self.id,
            'genre_id': self.genre_id,
            'image': self.artist_image,
        }

    # New instance instantiation procedure
        def __init__(self, artist_name, genre_id):
            self.artist_name = artist_name
            self.genre_id = genre_id
        self.artist_image = artist_image

        def __repr__(self):
            return '<Artist %r>' % (self.artist_name)


class Record(Base):

    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    artist_id = db.Column(db.Integer, ForeignKey('artist.id'))
    artist = db.relationship(Artist)
    genre_id = db.Column(db.Integer, ForeignKey('genre.id'), nullable=True)
    genre = db.relationship(Genre)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)
    record_image = db.Column(db.VARCHAR(200), nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'description': self.description,
            'artist_id':   self.artist_id,
            'genre_id': self.genre_id,
            'image': self.record_image,
        }
    # New instance instantiation procedure

        def __init__(self, title, artist_id, genre_id, year, description,
                     record_image):
            self.title = title
            self.artist_id = artist_id
            self.genre_id = genre_id
            self.year = year
            self.description = description
        self.record_image = record_image

        def __repr__(self):
            return '<Record %r>' % (self.title)
