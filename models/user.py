#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        __password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        __password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    if models.storage_t == 'db':
        @hybrid_property
        def password(self):
            return self.__password

        @password.setter
        def password(self, value):
            self.__password = hashlib.md5(value.encode()).hexdigest()
    else:
        @property
        def password(self):
            return self.__password

        @password.setter
        def password(self, value):
            self.__password = hashlib.md5(value.encode()).hexdigest()
