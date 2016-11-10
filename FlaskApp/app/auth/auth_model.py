from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from app import db

from app.records.record_model import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    # @property
    #   def serialize(self):
    #      """Return object data in easily serializeable format"""
    #      return {
    #          'name'         : self.name,
    #          'id'           : self.id,
    #          'email'        : self.email,
    #          'picture'      : self.picture,
    #      }
