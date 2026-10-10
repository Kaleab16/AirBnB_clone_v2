#!/usr/bin/python3
"""This module defines a base class for all hbnb models."""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models."""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        if 'created_at' in kwargs:
            if isinstance(kwargs['created_at'], str):
                kwargs['created_at'] = datetime.fromisoformat(
                    kwargs['created_at']
                )

        if 'updated_at' in kwargs:
            if isinstance(kwargs['updated_at'], str):
                kwargs['updated_at'] = datetime.fromisoformat(
                    kwargs['updated_at']
                )

        kwargs.pop('__class__', None)

        allowed = {'id', 'created_at', 'updated_at'}

        if hasattr(self, '__table__'):
            allowed.update(
                column.name for column in self.__table__.columns
            )

        if self.__class__ is BaseModel:
            allowed.update({
                'email', 'password', 'first_name', 'last_name',
                'name', 'state_id', 'city_id', 'user_id', 'place_id',
                'text', 'description', 'number_rooms',
                'number_bathrooms', 'max_guest', 'price_by_night',
                'latitude', 'longitude', 'amenity_ids'
            })

        for key in kwargs:
            if key not in allowed:
                raise KeyError(key)

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

        if hasattr(self, '__table__'):
            for column in self.__table__.columns:
                name = column.name

                if name in ('id', 'created_at', 'updated_at'):
                    continue

                if name in kwargs:
                    setattr(self, name, kwargs[name])
                elif name not in self.__dict__:
                    column_type = column.type.__class__.__name__

                    if column_type == 'String':
                        setattr(self, name, '')
                    elif column_type == 'Integer':
                        setattr(self, name, 0)
                    elif column_type == 'Float':
                        setattr(self, name, 0.0)

    def __str__(self):
        """Returns a string representation of the instance."""
        cls = type(self).__name__
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Update the timestamp and save the instance."""
        from models import storage

        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert the instance into a dictionary."""
        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state', None)

        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary

    def delete(self):
        """Delete the current instance from storage."""
        from models import storage

        storage.delete(self)
