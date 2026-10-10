#!/usr/bin/python3
"""City model for the HBNB project."""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """Represents a city belonging to a state."""

    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(
        String(60),
        ForeignKey('states.id'),
        nullable=False
    )

    state = relationship('State', back_populates='cities')

    def __init__(self, *args, **kwargs):
        """Initialize a City."""
        kwargs.setdefault('name', '')
        kwargs.setdefault('state_id', '')
        super().__init__(*args, **kwargs)
