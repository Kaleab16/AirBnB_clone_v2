#!/usr/bin/python3
""" State Module for HBNB project """

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class State(BaseModel):
    """ State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    cities = relationship(
        'City',
        backref='state',
        cascade='all, delete-orphan'
    )

    def __init__(self, *args, **kwargs):
        """Initialize a State."""
        if 'name' not in kwargs:
            kwargs['name'] = ''
        super().__init__(*args, **kwargs)
