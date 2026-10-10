#!/usr/bin/python3
"""State model for the HBNB project."""

from os import getenv

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """Represents a state containing cities."""

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            'City',
            back_populates='state',
            cascade='all, delete-orphan'
        )

    else:
        @property
        def cities(self):
            """Return cities belonging to this state in FileStorage."""
            from models import storage
            from models.city import City

            return [
                city for city in storage.all(City).values()
                if city.state_id == self.id
            ]

    def __init__(self, *args, **kwargs):
        """Initialize a State."""
        kwargs.setdefault('name', '')
        super().__init__(*args, **kwargs)
