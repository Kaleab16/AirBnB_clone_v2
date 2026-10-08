#!/usr/bin/python3
""" City Module for HBNB project """

from sqlalchemy import Column, ForeignKey, String

from models.base_model import BaseModel


class City(BaseModel):
    """ The city class, contains state ID and name """

    __tablename__ = 'cities'

    state_id = Column(
        String(60),
        ForeignKey('states.id'),
        nullable=False
    )
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a City."""
        if 'state_id' not in kwargs:
            kwargs['state_id'] = ''
        if 'name' not in kwargs:
            kwargs['name'] = ''
        super().__init__(*args, **kwargs)
