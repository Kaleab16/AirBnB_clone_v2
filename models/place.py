#!/usr/bin/python3
"""Place Module for HBNB project."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        primary_key=True,
        nullable=False
    ),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        primary_key=True,
        nullable=False
    )
)


class Place(BaseModel, Base):
    """A place to stay."""

    __tablename__ = 'places'

    city_id = Column(
        String(60),
        ForeignKey('cities.id'),
        nullable=False
    )
    user_id = Column(
        String(60),
        ForeignKey('users.id'),
        nullable=False
    )
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='place_amenities'
    )

    reviews = relationship(
        'Review',
        backref='place',
        cascade='all, delete-orphan'
    )

    def __init__(self, *args, **kwargs):
        """Initialize a Place."""
        defaults = {
            'city_id': '',
            'user_id': '',
            'name': '',
            'description': '',
            'number_rooms': 0,
            'number_bathrooms': 0,
            'max_guest': 0,
            'price_by_night': 0,
            'latitude': 0.0,
            'longitude': 0.0
        }

        for key, value in defaults.items():
            kwargs.setdefault(key, value)

        super().__init__(*args, **kwargs)

    @property
    def amenity_ids(self):
        """Return a list of amenity IDs."""
        return [amenity.id for amenity in self.amenities]
