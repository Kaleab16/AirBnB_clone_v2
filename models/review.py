#!/usr/bin/python3
"""Review module for HBNB project."""

from sqlalchemy import Column, ForeignKey, String

from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """Review class."""

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
        kwargs.setdefault('place_id', '')
        kwargs.setdefault('user_id', '')
        kwargs.setdefault('text', '')
        super().__init__(*args, **kwargs)
