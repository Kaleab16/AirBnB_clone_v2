#!/usr/bin/python3
"""This module defines a class User."""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes."""

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    places = relationship(
        'Place',
        backref='user',
        cascade='all, delete-orphan'
    )
    reviews = relationship(
        'Review',
        backref='user',
        cascade='all, delete-orphan'
    )

    def __init__(self, *args, **kwargs):
        """Initialize a User."""
        kwargs.setdefault('email', '')
        kwargs.setdefault('password', '')
        kwargs.setdefault('first_name', None)
        kwargs.setdefault('last_name', None)
        super().__init__(*args, **kwargs)
