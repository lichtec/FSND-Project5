# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json

from app.records.record_model import Base, Genre, Artist, Record

SQLALCHEMY_DATABASE_URI = "postgresql://catalog:Topher45%@localhost/catalog"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

f = open('config/testData.json')
parsedJson = json.loads(f.read())

for genre in parsedJson['genres']:
    newGenre = Genre(genre_name=genre['name'],
                    description=genre['description'],
                     genre_image=genre['image'])
    session.add(newGenre)
    session.commit()

print 'Genres added'

for artist in parsedJson['artists']:
    newArtist = Artist(artist_name=artist['name'],
                    genre_id=artist['genre_id'], artist_image=artist['image'])
    session.add(newArtist)
    session.commit()

print 'Artists added'

for record in parsedJson['records']:
    newRecord = Record(title=record['title'],
                       artist_id=record['artist_id'],
                       genre_id=record['genre_id'],
                       description=record['description'],
                       record_image=record['image'], year=record['year'])
    session.add(newRecord)
    session.commit()
print 'Records added'
session.close()
