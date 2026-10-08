#!/usr/bin/python3
""" Review module for the HBNB project """

from sqlalchemy import Column, ForeignKey, String

from models.base_model import BaseModel


class Review(BaseModel):
    """ Review class """

    __tablename__ = 'reviews'

    place_id = Column(
        String(60),
        ForeignKey('places.id'),
        nullable=False
    )
    user_id = Column(
        String(60),
        ForeignKey('users.id'),
        nullable=False
    )
    text = Column(String(1024), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a Review."""
        if 'place_id' not in kwargs:
            kwargs['place_id'] = ''
        if 'user_id' not in kwargs:
            kwargs['user_id'] = ''
        if 'text' not in kwargs:
            kwargs['text'] = ''
        super().__init__(*args, **kwargs)
