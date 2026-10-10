#!/usr/bin/python3
"""Amenity Module for HBNB project."""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """The amenity class."""

    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    place_amenities = relationship(
        'Place',
        secondary='place_amenity',
        back_populates='amenities'
    )

    def __init__(self, *args, **kwargs):
        """Initialize an Amenity."""
        kwargs.setdefault('name', '')
        super().__init__(*args, **kwargs)
